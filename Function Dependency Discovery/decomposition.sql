CREATE TABLE genres_new ( 
	genreId INT PRIMARY KEY, 
	genre VARCHAR(30)
);
INSERT INTO genres_new (genreId, genre)
	(SELECT genreId, genre
	 FROM new_relation_movie
	 GROUP BY genreId, genre);


CREATE TABLE movies_new (
	movieId INT PRIMARY KEY,
	type TEXT,
	startYear INT,
	runtime INT, 
	avgRating NUMERIC(3,1)
);
INSERT INTO movies_new (movieId, type, startYear, runtime, avgRating)
	(SELECT movieId, type, startYear, runtime, avgRating
	 FROM new_relation_movie
	 GROUP BY movieId, type, startYear, runtime, avgRating);

CREATE TABLE members_new (
	memberId INT PRIMARY KEY, 
	birthYear INT
);
INSERT INTO members_new (memberId, birthYear)
	(SELECT memberId, birthYear
	 FROM new_relation_movie
	 GROUP BY memberId, birthYear);

CREATE TABLE new_relation_movie_normalized (
	id INT PRIMARY KEY,
	genreId INT,
	movieId INT,
	memberId INT, 
	character INT,
	FOREIGN KEY (genreId) REFERENCES genres_new(genreId),
	FOREIGN KEY (movieId) REFERENCES movies_new(movieId),
	FOREIGN KEY (memberId) REFERENCES members_new(memberId)
);
INSERT INTO new_relation_movie_normalized (id, genreId, movieId, memberId, character)
	(SELECT id, genreId, movieId, memberId, character
	 FROM new_relation_movie
	 GROUP BY id, genreId, movieId, memberId, character);
	 
SELECT COUNT(*) FROM genres_new;
SELECT COUNT(*) FROM movies_new;
SELECT COUNT(*) FROM members_new;
SELECT COUNT(*) FROM new_relation_movie_normalized;
