SELECT MAX(name) AS AliveActor
FROM ((SELECT id, name
       FROM ComedyActor_Materialized
       WHERE deathyear is NULL)
UNION (SELECT id, name
       FROM NonComedyActor_Materialized
       WHERE deathyear is NULL)) aa
    INNER JOIN ActedIn_Materialized ai
    ON aa.id = ai.actor
    INNER JOIN ((SELECT id
                 FROM ComedyMovie_Materialized
                 WHERE year > 2000 and year < 2005)
                UNION (SELECT id
                       FROM NonComedyMovie_Materialized
                       WHERE year > 2000 and year < 2005)) am
    ON ai.title = am.id
GROUP BY aa.id
HAVING COUNT(am.id) > 10