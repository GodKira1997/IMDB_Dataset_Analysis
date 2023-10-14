CREATE VIEW All_Actor
AS
(SELECT *
FROM ComedyActor)
UNION
(SELECT *
 FROM NonComedyActor)