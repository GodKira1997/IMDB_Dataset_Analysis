-- Database: imdb

CREATE INDEX deathYear_index
ON member (deathYear ASC NULLS FIRST)

CREATE INDEX title_year_index
ON title (startYear ASC, endYear ASC)