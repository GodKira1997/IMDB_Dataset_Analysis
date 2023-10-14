CREATE MATERIALIZED VIEW NonComedyMovie_Materialized
AS
SELECT t.id AS id,
       t.title AS title,
       t.startyear AS year
FROM title t
    LEFT JOIN (SELECT title
                    FROM title_genre tg
                        INNER JOIN (SELECT genre.id,
                                           genre.genre
                                    FROM genre
                                    WHERE genre.genre = 'Comedy') g
                            ON g.id = tg.genre) tgg
        ON t.id = tgg.title
WHERE t.runtime > 75
  AND tgg.title IS NULL
WITH DATA;
