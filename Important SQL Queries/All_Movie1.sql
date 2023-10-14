CREATE VIEW All_Movie
AS
(SELECT id, title, year, 'Comedy'
    AS genre
FROM ComedyMovie)
UNION
(SELECT id, title, year,
        'Non-Comedy' AS genre
 FROM NonComedyMovie)