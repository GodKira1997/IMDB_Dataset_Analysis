CREATE MATERIALIZED VIEW NonComedyActor_Materialized
AS
SELECT m.id AS id,
       name,
       birthYear,
       deathYear
FROM member m
    LEFT JOIN (SELECT actor
               FROM title_actor ta
                   INNER JOIN title t
                       ON t.id = ta.title
                   INNER JOIN title_genre tg
                       ON t.id = tg.title
                   INNER JOIN (SELECT genre.id,
                                      genre.genre
                               FROM genre
                               WHERE genre.genre = 'Comedy') g
                    ON g.id = tg.genre
               WHERE t.runtime > 75) a
        ON m.id = a.actor
WHERE a.actor is NULL
WITH DATA;