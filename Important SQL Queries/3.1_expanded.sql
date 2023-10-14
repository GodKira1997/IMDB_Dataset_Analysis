SELECT MAX(name) AS AliveActor
FROM ((SELECT *
       FROM ComedyActor)
UNION (SELECT *
       FROM NonComedyActor)) aa
    INNER JOIN (SELECT *
                FROM ActedIn) ai
    ON aa.id = ai.actor
    INNER JOIN (SELECT id
                FROM ((SELECT id, title, year, 'Comedy' AS genre
                       FROM ComedyMovie)
                UNION (SELECT id, title, year, 'Non-Comedy' AS genre
                       FROM NonComedyMovie)) movies
                WHERE year > 2000 and year < 2005) am
    ON ai.title = am.id
WHERE deathyear is NULL
GROUP BY aa.id
HAVING COUNT(am.id) > 10