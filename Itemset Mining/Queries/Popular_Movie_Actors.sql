DROP TABLE IF EXISTS Popular_Movie_Actors;

CREATE TABLE Popular_Movie_Actors AS
    SELECT ta.title AS title, actor
    FROM title_actor ta
        INNER JOIN title t
            ON t.id = ta.title
    WHERE type = 'movie' AND avgrating > 5
    ORDER BY actor;

SELECT * FROM Popular_Movie_Actors;