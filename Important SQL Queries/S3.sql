CREATE VIEW ComedyActor
AS
SELECT DISTINCT m.id AS id,
       name,
       birthYear,
       deathYear
FROM member m
    INNER JOIN title_actor ta
        ON m.id = ta.actor
    INNER JOIN title t
        ON t.id = ta.title
    INNER JOIN title_genre tg
        ON t.id = tg.title
    INNER JOIN (SELECT genre.id,
                       genre.genre
                FROM genre
                WHERE genre.genre = 'Comedy') g
        ON g.id = tg.genre
WHERE t.runtime > 75;