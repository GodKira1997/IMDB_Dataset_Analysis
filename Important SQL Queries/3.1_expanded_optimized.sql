SELECT MAX(name) AS AliveActor
FROM ((SELECT id, name
       FROM ComedyActor
       WHERE deathyear is NULL)
UNION (SELECT id, name
       FROM NonComedyActor
       WHERE deathyear is NULL)) aa
    INNER JOIN ActedIn ai
    ON aa.id = ai.actor
    INNER JOIN ((SELECT id
                 FROM ComedyMovie
                 WHERE year > 2000 and year < 2005)
                UNION (SELECT id
                       FROM NonComedyMovie
                       WHERE year > 2000 and year < 2005)) am
    ON ai.title = am.id
GROUP BY aa.id
HAVING COUNT(am.id) > 10