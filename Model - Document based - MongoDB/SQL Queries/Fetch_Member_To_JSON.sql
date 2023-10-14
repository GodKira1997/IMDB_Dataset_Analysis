SELECT JSON_STRIP_NULLS(ROW_TO_JSON(results))
FROM (
	SELECT id AS _id, name, birthyear, deathyear
	FROM member
) results