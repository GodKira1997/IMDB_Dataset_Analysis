-- Database: imdb

SELECT DISTINCT m.name AS Alive_Actors
FROM (SELECT * FROM member
	  WHERE name LIKE 'Phi%' 
	  	AND deathyear IS NULL) AS m
INNER JOIN title_actor as ta
ON ta.actor = m.id
INNER JOIN title as t
ON ta.title = t.id
WHERE (t.startyear > 2014 
	   OR 
	   (CASE WHEN t.type LIKE 'tv%'
		THEN (CASE WHEN t.startyear < 2014 
			  THEN (t.endyear < 2014)
			  ELSE false END)
		ELSE false END));
