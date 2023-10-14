DROP TABLE IF EXISTS L1;

CREATE TABLE L1 AS
    SELECT p1.actor AS actor1, COUNT(p1.title) AS count
    FROM Popular_Movie_Actors p1
    GROUP BY p1.actor
    HAVING COUNT(p1.title) >= 5;

SELECT * FROM L1;