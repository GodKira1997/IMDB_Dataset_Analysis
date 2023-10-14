CREATE VIEW
    All_Actor_From_Materialized
AS
(SELECT *
FROM ComedyActor_Materialized)
UNION
(SELECT *
 FROM NonComedyActor_Materialized)