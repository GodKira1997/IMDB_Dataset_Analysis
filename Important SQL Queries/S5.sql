CREATE VIEW ActedIn
AS
SELECT actor, ta.title AS title
FROM title_actor ta
   INNER JOIN title t
       ON t.id = ta.title
WHERE t.runtime > 75;