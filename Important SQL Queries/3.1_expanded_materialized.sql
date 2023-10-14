SELECT MAX(name) AS AliveActor
FROM ((SELECT *
       FROM comedyactor_materialized)
UNION (SELECT *
       FROM noncomedyactor_materialized)) aa
    INNER JOIN (SELECT *
                FROM actedin_materialized) ai
    ON aa.id = ai.actor
    INNER JOIN (SELECT id
                FROM ((SELECT id, title, year, 'Comedy' AS genre
                       FROM comedymovie_materialized)
                UNION (SELECT id, title, year, 'Non-Comedy' AS genre
                       FROM noncomedymovie_materialized)) movies
                WHERE year > 2000 and year < 2005) am
    ON ai.title = am.id
WHERE deathyear is NULL
GROUP BY aa.id
HAVING COUNT(am.id) > 10