-- get average from rating from ratings joining with movies table to get the year filter
SELECT AVG(rating) FROM ratings
JOIN movies ON ratings.movie_id = movies.id
WHERE year = 2012;