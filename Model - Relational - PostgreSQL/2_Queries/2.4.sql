-- Database: imdb

SELECT name AS Alive_Producer, t.runtime AS runtime
FROM title_producer AS p
INNER JOIN member AS m
ON p.producer = m.id
INNER JOIN title AS t
ON t.id = p.title
WHERE t.runtime > 120
	AND deathYear is NULL
ORDER BY t.runtime DESC;