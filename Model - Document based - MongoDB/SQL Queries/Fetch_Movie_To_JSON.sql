SELECT JSON_STRIP_NULLS(ROW_TO_JSON(results))
FROM (SELECT id, type, t.title AS title, originalTitle, startYear, endYear, runtime, avgRating, numVotes,
	genres, actors, directors, writers, producers
	FROM title AS t
	LEFT JOIN (SELECT title, ARRAY_AGG(g.genre) AS genres 
				FROM title_genre AS tg 
				INNER JOIN genre AS g 
				ON g.id = tg.genre 
				GROUP BY title) AS g
	ON t.id = g.title
	LEFT JOIN (SELECT title, ARRAY_AGG(writer) AS writers 
				FROM title_writer 
				GROUP BY title) AS w
	ON t.id = w.title
	LEFT JOIN (SELECT title, ARRAY_AGG(director) AS directors 
			   FROM title_director 
			   GROUP BY title) AS d
	ON t.id = d.title
	LEFT JOIN (SELECT title, ARRAY_AGG(producer) AS producers 
			   FROM title_producer 
			   GROUP BY title) AS p
	ON t.id = p.title
	LEFT JOIN (SELECT title, JSON_AGG(JSON_BUILD_OBJECT(
				   'actor', actor, 
				   'roles', characters)) AS actors 
			   FROM ( 
				   SELECT title, actor, ARRAY_AGG(c.character) AS characters 
				   FROM actor_title_character AS atc 
				   INNER JOIN character AS c 
				   ON atc.character = c.id 
				   GROUP BY title, actor) AS ta
			   GROUP BY title) AS a
	ON t.id = a.title
) results