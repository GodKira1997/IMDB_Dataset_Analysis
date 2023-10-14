SELECT MAX(name) AS AliveActor
FROM all_actor aa
    INNER JOIN all_movie_actor ama
    ON aa.id = ama.actor
    INNER JOIN (SELECT id
                FROM all_movie
                WHERE year > 2000 and year < 2005) am
    ON ama.title = am.id
WHERE deathyear is NULL
GROUP BY aa.id
HAVING COUNT(am.id) > 10