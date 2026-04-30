class TestPostMovies:

    def test_post_movies(self, api_manager, rand_movie):
        api_manager.auth_api.authenticate()
        movie = rand_movie()
        response = api_manager.movies_api.post_movies(movie)

        data = response.json()
        assert data["name"] == movie["name"]
        assert data["price"] == movie["price"]
        assert data["description"] == movie["description"]

        response = api_manager.movies_api.get_movie_with_id(data["id"])
        data = response.json()
        assert data["name"] == movie["name"]
        assert data["price"] == movie["price"]
        assert data["description"] == movie["description"]