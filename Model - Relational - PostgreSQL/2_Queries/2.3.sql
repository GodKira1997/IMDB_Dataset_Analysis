-- Database: imdb

SELECT m.name AS Producer, g.genre AS genre, COUNT(tg.title) AS numOfShows
FROM title_producer AS p
INNER JOIN member AS m
ON p.producer = m.id
INNER JOIN title_genre AS tg
ON tg.title = p.title
INNER JOIN genre AS g
ON g.id = tg.genre
INNER JOIN title AS t
ON t.id = p.title
WHERE g.genre = 'Talk-Show'
	AND name ILIKE '%gill%'
	AND (t.startyear = 2017)
GROUP BY (name, g.genre)
ORDER BY numOfShows DESC;