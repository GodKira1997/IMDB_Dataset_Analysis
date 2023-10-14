"""
file: load_data.py
description: This program process the TSV files and insert data to the
already existing imdb database and tables
language: python3
author: Anurag Kallurwar, ak6491@rit.edu
"""

from time import perf_counter
import configparser as configparser

import numpy as np
import psycopg2
import psycopg2.extras
import numpy
import pandas


def parse_ini(section: str) -> dict:
    """
    This function parses ini file for configuration details
    :param section: section to read from ini
    :return: Dictionary of config details
    """
    config = dict()
    parser = configparser.ConfigParser()
    parser.read("imdb_database.ini")
    if parser.has_section(section):
        config_items = parser.items(section)
        for item in config_items:
            config[item[0]] = item[1]
    return config


def create_nulls(dataframe: pandas.DataFrame) -> pandas.DataFrame:
    """
    This function converts the null values to None type in dataframe
    :param dataframe: dataframe
    :return: dataframe
    """
    dataframe = dataframe.astype(str)
    dataframe.replace({None: '\\N', 'nan': '\\N'}, inplace=True)
    return dataframe


def create_csv(dataframe: pandas.DataFrame, csv_name: str) -> str:
    """
    This function creates and load cs using a dataframe
    :param dataframe: input dataframe
    :param csv_name: Name for CSV
    :return: Name of CSV
    """
    print("CSV: " + csv_name)
    dataframe.to_csv(csv_name + ".csv", sep='|', na_rep='\\N',
                     float_format='%.1f', index=False)
    return csv_name


def process_data(input_config: dict, list_of_csvs: list) -> None:
    """
    This function reads and process the data using pandas dataframes
    :param list_of_csvs: list of output CSVs
    :param input_config: Input TSV details
    :return: None
    """
    null_values = [np.nan, 'nan', '\\N', '', None]

    start = perf_counter()
    # READING & PROCESSING title.basics.tsv
    print("\nREADING & PROCESSING title.basics")
    df_titles = pandas.read_csv(input_config['titlebasics'], sep="\t",
                                low_memory=False)
    df_titles.drop(df_titles[df_titles['titleType'].isin([
        'tvepisode', ['tvEpisode']])].index, inplace=True)
    df_titles.drop(df_titles[df_titles['primaryTitle'].isin(
        null_values)].index, inplace=True)
    df_titles.drop(df_titles[df_titles['isAdult'].isin(
        null_values + ['1'])].index, inplace=True)
    df_titles['tconst'] = df_titles['tconst'].apply(lambda x: int(x[2:]))
    df_titles['genres'] = df_titles['genres'].apply(lambda x: str(x).split(','))
    df_titles['runtimeMinutes'] = (df_titles['runtimeMinutes']).apply(
        pandas.to_numeric, errors='coerce')
    df_titles['runtimeMinutes'] = df_titles['runtimeMinutes'].replace(
        numpy.nan, 0, regex=True)
    df_titles['runtimeMinutes'] = df_titles['runtimeMinutes'].astype(int)

    print(perf_counter() - start)
    start = perf_counter()

    # CREATING title_genres dataframe from df_titles
    print("\nCREATING title_genres dataframe")
    df_title_genres = df_titles.drop(['titleType', 'primaryTitle',
                                      'originalTitle', 'isAdult', 'startYear',
                                      'endYear', 'runtimeMinutes'],
                                     axis=1).explode('genres')
    df_title_genres.drop(df_title_genres[df_title_genres['genres'].isin(
        null_values)].index, inplace=True)

    # CREATING genres dataframe from df_title_genres
    print("CREATING genres dataframe")
    genres = df_title_genres['genres'].unique()
    df_genres = pandas.DataFrame(genres)
    df_genres['genreId'] = pandas.RangeIndex(0, len(df_genres)) + 1
    df_genres.rename(columns={0: 'genre'}, inplace=True)

    # REPLACING title_genres dataframe's column genre to genreId"
    print("REPLACING title_genres dataframe's column genre to genreId")
    df_title_genres = pandas.merge(df_title_genres, df_genres, how='inner',
                                   left_on='genres', right_on='genre').drop([
        'genres', 'genre'], axis=1)
    df_title_genres.drop(df_title_genres[df_title_genres['tconst'].isin(
        null_values)].index, inplace=True)

    print(perf_counter() - start)
    start = perf_counter()

    # READING & PROCESSING title.ratings.tsv
    print("\nREADING & PROCESSING title.ratings")
    df_titles_ratings = pandas.read_csv(input_config['titleratings'], sep="\t")
    df_titles_ratings['tconst'] = df_titles_ratings['tconst'].apply(lambda x:
                                                                    int(x[2:]))
    df_titles_ratings['numVotes'] = df_titles_ratings['numVotes'].astype(int)
    df_titles_ratings['numVotes'] = df_titles_ratings['numVotes'].astype(object)

    # MERGING ratings dataframe to titles dataframe and removing unnecessary
    # columns
    print("MERGING ratings dataframe to titles dataframe")
    df_titles = df_titles.drop(['genres', 'isAdult'], axis=1)
    df_titles = pandas.merge(df_titles, df_titles_ratings, how='left',
                             on='tconst')
    df_titles = create_nulls(df_titles)
    df_titles.drop(df_titles[df_titles['primaryTitle'].isin([None])].index,
                   inplace=True)
    df_tconst = pandas.DataFrame(df_titles['tconst']).astype(int)

    print(perf_counter() - start)

    df_title_genres = pandas.merge(df_tconst, df_title_genres, how='inner',
                                   on='tconst')
    df_title_genres = df_title_genres.astype(object)

    # Renaming
    df_titles.rename(columns={'tconst': 'id', 'titleType': 'type',
                              'primaryTitle': 'title', 'runtimeMinutes':
                                  'runtime', "averageRating": "avgRating"},
                     inplace=True)
    df_genres.rename(columns={'genreId': 'id'}, inplace=True)
    df_title_genres.rename(columns={'tconst': 'title', 'genreId': 'genre'},
                           inplace=True)

    start = perf_counter()

    # READING & PROCESSING name.basics.tsv
    print("\nREADING & PROCESSING name.basics")
    df_names = pandas.read_csv(input_config['namebasics'], sep="\t",
                               usecols=['nconst', 'primaryName', 'birthYear',
                                        'deathYear'])
    df_names.drop(df_names[df_names['primaryName'].isin(
        null_values)].index, inplace=True)
    df_names['nconst'] = df_names['nconst'].apply(lambda x: int(x[2:]))
    df_names = create_nulls(df_names)
    df_names.drop(df_names[df_names['primaryName'].isin([None])].index,
                  inplace=True)
    df_nconst = pandas.DataFrame(df_names['nconst']).astype(int)

    # Renaming
    df_names.rename(columns={'nconst': 'id', 'primaryName': 'name'},
                    inplace=True)

    print(perf_counter() - start)
    start = perf_counter()

    # READING & PROCESSING title.crew.tsv
    print("\nREADING & PROCESSING title.crew")
    df_titles_crew = pandas.read_csv(input_config['titlecrew'], sep="\t")
    df_titles_crew['tconst'] = df_titles_crew['tconst'].apply(lambda x: int(
        x[2:]))

    print(perf_counter() - start)
    start = perf_counter()

    # CREATING directors dataframe from title.crew.csv
    print("\nCREATING directors dataframe")
    df_directors = df_titles_crew.drop(['writers'], axis=1)
    df_directors['directors'] = df_directors['directors'].apply(lambda x:
                                                                str(x).split(
                                                                    ','))
    df_directors = df_directors.explode('directors')
    df_directors.drop(df_directors[df_directors['directors'].isin(
        null_values)].index, inplace=True)
    df_directors.rename(columns={'directors': 'nconst'}, inplace=True)
    df_directors['nconst'] = df_directors['nconst'].apply(lambda x: int(x[2:]))
    df_directors = pandas.merge(df_tconst, df_directors, how='inner',
                                on='tconst')
    df_directors = pandas.merge(df_nconst, df_directors, how='inner',
                                on='nconst')
    df_directors = (df_directors.drop_duplicates()).astype(object)
    df_directors.rename(columns={'tconst': 'title', 'nconst': 'director'},
                        inplace=True)

    print(perf_counter() - start)
    start = perf_counter()

    # CREATING writers dataframe from title.crew.csv
    print("\nCREATING writers dataframe")
    df_writers = df_titles_crew.drop(['directors'], axis=1)
    df_writers['writers'] = df_writers['writers'].apply(lambda x: str(
        x).split(','))
    df_writers = df_writers.explode('writers')
    df_writers.drop(df_writers[df_writers['writers'].isin(
        null_values)].index, inplace=True)
    df_writers.rename(columns={'writers': 'nconst'}, inplace=True)
    df_writers['nconst'] = df_writers['nconst'].apply(lambda x: int(x[2:]))
    df_writers = pandas.merge(df_tconst, df_writers, how='inner',
                              on='tconst')
    df_writers = pandas.merge(df_nconst, df_writers, how='inner',
                              on='nconst')
    df_writers = (df_writers.drop_duplicates()).astype(object)
    df_writers.rename(columns={'tconst': 'title', 'nconst': 'writer'},
                      inplace=True)

    print(perf_counter() - start)
    start = perf_counter()

    # READING & PROCESSING title.principals.tsv
    print("\nREADING & PROCESSING title.principals")
    df_titles_principals = pandas.read_csv(input_config['titleprincipals'],
                                           sep="\t", usecols=['tconst',
                                                              'nconst',
                                                              'category',
                                                              'characters'])
    df_titles_principals.drop(df_titles_principals[df_titles_principals[
        'nconst'].isin(null_values)].index, inplace=True)
    df_titles_principals.drop(df_titles_principals[df_titles_principals[
        'tconst'].isin(null_values)].index, inplace=True)
    df_titles_principals['tconst'] = df_titles_principals['tconst'].apply(
        lambda x: int(x[2:]))
    df_titles_principals['nconst'] = df_titles_principals['nconst'].apply(
        lambda x: int(x[2:]))

    print(perf_counter() - start)
    start = perf_counter()

    # CREATING df_actors_title_characters dataframe from title.principals.tsv
    print("\nCREATING actors_title_characters dataframe")
    df_actors_title_characters = pandas.DataFrame(df_titles_principals[
                                                      df_titles_principals[
                                                        'category'].isin([
                                                          'actor', 'self',
                                                          'actress'])]).drop([
                                                            'category'], axis=1)
    df_actors_title_characters = pandas.merge(df_tconst,
                                              df_actors_title_characters,
                                              how='inner', on='tconst')
    df_actors_title_characters = pandas.merge(df_nconst,
                                              df_actors_title_characters,
                                              how='inner', on='nconst')
    df_actors_title_characters = (df_actors_title_characters.drop_duplicates(
    ))

    print(perf_counter() - start)
    start = perf_counter()

    # CREATING actors dataframe from df_actors_title_characters
    print("\nCREATING actors dataframe")
    df_actors = df_actors_title_characters.drop(['characters'], axis=1)
    df_actors = (df_actors.drop_duplicates()).astype(object)

    print(perf_counter() - start)
    start = perf_counter()

    # CREATING characters dataframe from df_actors_title_characters
    print("\nCREATING characters dataframe")
    df_actors_title_characters['characters'] = df_actors_title_characters[
        'characters'].apply(lambda x: str(x).strip('[').strip(']').split(','))
    df_actors_title_characters = df_actors_title_characters.explode(
        'characters')
    df_actors_title_characters.drop(df_actors_title_characters[
                                        df_actors_title_characters[
                                            'characters'].isin(
                                            null_values)].index, inplace=True)
    characters = df_actors_title_characters['characters'].unique()
    df_characters = pandas.DataFrame(characters)
    df_characters.rename(columns={0: 'character'},
                         inplace=True)
    df_characters['id'] = pandas.RangeIndex(0, len(df_characters)) + 1
    df_characters = (df_characters.drop_duplicates())

    print(perf_counter() - start)
    start = perf_counter()

    # REPLACING df_actors_title_characters dataframe's column characters to
    # id's
    print("\nREPLACING actors_title_characters dataframe's column characters "
          "to character Id")
    df_actors_title_characters = pandas.merge(df_actors_title_characters,
                                              df_characters, how='inner',
                                              left_on='characters',
                                              right_on='character').drop([
                                                'characters', 'character'],
        axis=1)
    df_actors_title_characters.drop(df_actors_title_characters[
                                        df_actors_title_characters[
                                            'tconst'].isin(null_values)].index,
                                    inplace=True)
    df_actors_title_characters.drop(df_actors_title_characters[
                                        df_actors_title_characters[
                                            'nconst'].isin(null_values)].index,
                                    inplace=True)
    df_actors_title_characters.drop(df_actors_title_characters[
                                        df_actors_title_characters[
                                            'id'].isin(null_values)].index,
                                    inplace=True)
    df_actors_title_characters = (df_actors_title_characters.drop_duplicates(
    )).astype(object)

    # Renaming
    df_actors.rename(columns={'tconst': 'title', 'nconst': 'actor'},
                     inplace=True)
    df_actors_title_characters.rename(columns={'tconst': 'title', 'nconst':
        'actor', 'id': 'character'}, inplace=True)
    df_characters['character'] = df_characters['character'].apply(lambda x:
                                                                  str(x).strip('"').strip('\\').strip())
    df_characters['character'] = df_characters['character'].apply(lambda x:
                                                                  str(x).replace('|', ':'))

    print(perf_counter() - start)
    start = perf_counter()

    # CREATING producers dataframe from title.principals.tsv
    print("\nCREATING producers dataframe")
    df_producers = pandas.DataFrame(df_titles_principals[df_titles_principals[
        'category'].isin(['producer'])]).drop(['category', 'characters'],
                                              axis=1)
    df_producers = pandas.merge(df_tconst, df_producers, how='inner',
                                on='tconst')
    df_producers = pandas.merge(df_nconst, df_producers, how='inner',
                                on='nconst')
    df_producers = (df_producers.drop_duplicates()).astype(object)
    df_producers.rename(columns={'tconst': 'title', 'nconst': 'producer'},
                        inplace=True)

    print(perf_counter() - start)
    start = perf_counter()

    df_genres = df_genres.iloc[:, [1, 0]]
    df_characters = df_characters.iloc[:, [1, 0]]
    df_actors_title_characters = df_actors_title_characters.iloc[:, [1, 0, 2]]
    df_directors = df_directors.iloc[:, [1, 0]]
    df_producers = df_producers.iloc[:, [1, 0]]
    df_writers = df_writers.iloc[:, [1, 0]]
    df_actors = df_actors.iloc[:, [1, 0]]

    print(df_genres.head(2))
    print(df_titles.head(2))
    print(df_title_genres.head(2))
    print(df_names.head(2))
    print(df_directors.head(2))
    print(df_producers.head(2))
    print(df_writers.head(2))
    print(df_actors.head(2))
    print(df_characters.head(2))
    print(df_actors_title_characters.head(2))

    print("\nCreate CSVs")
    create_csv(df_genres, list_of_csvs[0])
    create_csv(df_titles, list_of_csvs[1])
    create_csv(df_title_genres, list_of_csvs[2])
    create_csv(df_names, list_of_csvs[3])
    create_csv(df_directors, list_of_csvs[4])
    create_csv(df_producers, list_of_csvs[5])
    create_csv(df_writers, list_of_csvs[6])
    create_csv(df_actors, list_of_csvs[7])
    create_csv(df_characters, list_of_csvs[8])
    create_csv(df_actors_title_characters, list_of_csvs[9])

    print(perf_counter() - start)


def load_entities(db_config: dict, list_of_csvs: list) -> bool:
    """
    This function insert dataframe to an existing entity table
    :param db_config: Database configuration details
    :param list_of_csvs:
    :return: boolean whether process was done or not
    """
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    for csv_name in list_of_csvs:
        try:
            with open(csv_name + '.csv', 'r', encoding='utf-8') as csvfile:
                next(csvfile)  # To skip header row.
                start = perf_counter()
                print("Copying from CSV:" + csv_name + " to DB")
                cursor.copy_from(csvfile, csv_name, sep='|', null='\\N')
                conn.commit()
                print(perf_counter() - start)
                print("The CSV is loaded to DB")
        except (Exception, psycopg2.DatabaseError) as error:
            print("SQL Exception:" + str(error))
            conn.rollback()
            return False
    cursor.close()
    conn.close()
    return True


def main() -> None:
    """
    The main function
    :return: None
    """
    # Reading "imdb_database.ini" file
    db_config = parse_ini("postgresql")
    input_config = parse_ini("data")
    print("INI Info:")
    print("postgresql: ", end=" ")
    print(db_config)
    print("data: ", end=" ")
    print(input_config)

    list_of_csvs = ["genre", "title", "title_genre", "member",
                    "title_director", "title_producer", "title_writer",
                    "title_actor", "character", "actor_title_character"]

    # Processing Data
    start = perf_counter()
    process_data(input_config, list_of_csvs)
    print("\nProcess Data Running Time: " + str(perf_counter() - start))

    # Inserting all entity tables and relation tables
    print("\nINSERTING data from dataframes to tables in IMDB DB")
    start = perf_counter()
    load_entities(db_config, list_of_csvs)
    print("Process Data Running Time: " + str(perf_counter() - start))
    print("INSERTION of data Completed")


main()
