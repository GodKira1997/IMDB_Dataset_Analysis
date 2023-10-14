SELECT name AS Actor
FROM ((SELECT *
       FROM comedyactor_materialized)
UNION (SELECT *
       FROM noncomedyactor_materialized)) aa
    LEFT JOIN (SELECT actor
               FROM (SELECT *
                     FROM actedin_materialized) ama
                   INNER JOIN (SELECT id
                               FROM ((SELECT id, title, year, 'Comedy' AS genre
                                      FROM comedymovie_materialized)
                               UNION (SELECT id, title, year, 'Non-Comedy' AS genre
                                      FROM noncomedymovie_materialized)) movies
                               WHERE genre = 'Comedy') am
                       ON ama.title = am.id) a
        ON aa.id = a.actor
WHERE name LIKE 'Ja%' and a.actor is NULL