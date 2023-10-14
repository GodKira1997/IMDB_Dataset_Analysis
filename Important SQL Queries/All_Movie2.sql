CREATE VIEW
    All_Movie_From_Materialized
AS
(SELECT id, title, year,
        'Comedy' AS genre
FROM ComedyMovie_Materialized)
UNION
(SELECT id, title, year,
        'Non-Comedy' AS genre
 FROM NonComedyMovie_Materialized)