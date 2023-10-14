SELECT name AS Actor
FROM ((SELECT *
       FROM ComedyActor)
UNION (SELECT *
       FROM NonComedyActor)) aa
    LEFT JOIN (SELECT actor
               FROM (SELECT *
                     FROM ActedIn) ama
                   INNER JOIN (SELECT id
                               FROM ((SELECT id, title, year, 'Comedy' AS genre
                                      FROM ComedyMovie)
                               UNION (SELECT id, title, year, 'Non-Comedy' AS genre
                                      FROM NonComedyMovie)) movies
                               WHERE genre = 'Comedy') am
                       ON ama.title = am.id) a
        ON aa.id = a.actor
WHERE name LIKE 'Ja%' and a.actor is NULL