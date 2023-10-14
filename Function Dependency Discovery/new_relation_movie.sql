-- Database: imdb

-- 25046174

DROP TABLE IF EXISTS new_relation_movie;
CREATE TABLE new_relation_movie (
	id SERIAL PRIMARY KEY,
	movieId INT,
	type TEXT,
	startYear INT,
	runtime INT, 
	avgRating NUMERIC(3,1), 
	genreId INT, 
	genre VARCHAR(30), 
	memberId INT, 
	birthYear INT, 
	character INT
);

INSERT INTO new_relation_movie (movieId, type, startYear, 
								runtime, avgRating,genreId, 
								genre, memberId, birthYear, 
								character) 
	(SELECT atc.title AS movieId, type, startYear, runtime, 
	avgRating, g.id as genreId, g.genre AS genre, memberId, 
	birthYear, character 
	FROM (
		SELECT title, actor, MAX(character) AS character
		FROM actor_title_character
		GROUP BY title, actor
		HAVING COUNT(character) = 1
	) AS atc
	INNER JOIN (
		SELECT id AS memberId, birthYear
		FROM member
	) AS m
	ON atc.actor = m.memberId
	INNER JOIN (
		SELECT id, type, startYear, runtime, avgRating
		FROM title
		WHERE runtime >= 90
	) AS t
	ON atc.title = t.id
	INNER JOIN title_genre AS tg
	ON t.id = tg.title
	INNER JOIN genre AS g
	ON tg.genre = g.id
);
	