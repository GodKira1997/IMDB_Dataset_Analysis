-- Database: imdb

SELECT COUNT(*) AS Invalid_Title_Actor
FROM title_actor AS ta
LEFT JOIN actor_title_character AS atc
ON ta.actor = atc.actor AND ta.title = atc.title
WHERE character IS NULL;
