SELECT name AS Actor
FROM all_actor aa
    LEFT JOIN (SELECT actor
               FROM all_movie_actor ama
                   INNER JOIN (SELECT id
                               FROM all_movie
                               WHERE genre = 'Comedy') am
                       ON ama.title = am.id) a
        ON aa.id = a.actor
WHERE name LIKE 'Ja%' and a.actor is NULL