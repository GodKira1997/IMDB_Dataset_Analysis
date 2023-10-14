-- Database: imdb

SELECT DISTINCT name AS Alive_Actor
FROM member AS m
INNER JOIN actor_title_character AS atc
ON m.id = atc.actor
INNER JOIN character as c
ON c.id = atc.character
WHERE deathYear is NULL 
	AND c.character = 'Jesus Christ';