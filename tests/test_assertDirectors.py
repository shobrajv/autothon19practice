import pytest
from ..AssertDirectors import AssertDirectors


class TestAssertDirectors:
    def test_assert_directors(self):
        movies = [#"Non-Existing", "The Shawshank Redemption", "The Godfather", "The Dark Knight", "Pulp Fiction", "Schindler's List",
        "The Lord of the Rings: The Return of the King", "The Good, The Bad, The Ugly", "12 Angry men"]#, "Incpetion",
        # "Forrrest Gump", "Star Wars: Episode V - The Empire Strikes Back", "Goodfellas", "The Matrix",
        # "One Flew Over the Cuckoo's Nest", "Seven Samurai", "Avengers: Infinity War", "Se7en"]

        sites = ["wikipedia.org", "imdb.com"]

        def assert_directors(movie_directors_dict):
            for movie in movie_directors_dict.keys():
                if not None in movie_directors_dict[movie].values():
                    if movie_directors_dict[movie]['wikipedia.org'][1] == movie_directors_dict[movie]['imdb.com'][1]:
                        print(f"Director: {movie_directors_dict[movie]['imdb.com'][1]} match for Movie: {movie}")
                    else:
                        print(f"Director: {movie_directors_dict[movie]['imdb.com'][1]} dosen't match for Movie: {movie}")
                else:
                    print(f"{movie} is not a valid movie")

        assert_dirs_obj = AssertDirectors(movies, sites)
        assert_dirs = assert_dirs_obj.get_movie_directors()
        assert_directors(assert_dirs)