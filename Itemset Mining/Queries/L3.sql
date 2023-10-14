DROP TABLE IF EXISTS L3;

CREATE TABLE L3 AS
    SELECT p1.actor AS actor1, p2.actor AS actor2, p3.actor AS actor3, COUNT(p1.title) AS count
    FROM Popular_Movie_Actors p1
        INNER JOIN Popular_Movie_Actors p2
            ON p1.title = p2.title
                   AND p1.actor < p2.actor
        INNER JOIN Popular_Movie_Actors p3
            ON p2.title = p3.title
                   AND p2.actor < p3.actor
    GROUP BY p1.actor, p2.actor, p3.actor
    HAVING COUNT(p1.title) >= 5;

SELECT * FROM L3;