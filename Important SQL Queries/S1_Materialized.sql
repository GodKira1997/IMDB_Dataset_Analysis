CREATE MATERIALIZED VIEW ComedyMovie_Materialized
AS
SELECT t.id AS id,
       t.title AS title,
       t.startyear AS year
FROM title t
    INNER JOIN title_genre tg
        ON t.id = tg.title
    INNER JOIN (SELECT genre.id,
                       genre.genre
                FROM genre
                WHERE genre.genre = 'Comedy') g
        ON g.id = tg.genre
WHERE t.runtime > 75
WITH DATA;