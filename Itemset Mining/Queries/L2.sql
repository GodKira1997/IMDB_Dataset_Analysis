DROP TABLE IF EXISTS L2;

CREATE TABLE L2 AS
    SELECT p1.actor AS actor1, p2.actor AS actor2, COUNT(p1.title) AS count
    FROM Popular_Movie_Actors p1
        INNER JOIN Popular_Movie_Actors p2
            ON p1.title = p2.title
                   AND p1.actor < p2.actor
    GROUP BY p1.actor, p2.actor
    HAVING COUNT(p1.title) >= 5;

SELECT * FROM L2;