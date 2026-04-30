class TestPatchMoviesId:
    def test_patch_movie(self, api_manager, rand_movie):
        api_manager.auth_api.authenticate()
        response = api_manager.movies_api.post_movies(rand_movie())

        data = response.json()
        film_id = data["id"]

        rand_movie = rand_movie()

        response = api_manager.movies_api.patch_movie_with_id(film_id, rand_movie)
        assert response.json()["id"] == film_id
        assert response.json()["name"] == rand_movie["name"]

    def test_patch_movie_description(self, api_manager, rand_movie):
        api_manager.auth_api.authenticate()
        response = api_manager.movies_api.post_movies(rand_movie())

        data = response.json()
        film_id = data["id"]

        description = {"description": "Patched"}

        response = api_manager.movies_api.patch_movie_with_id(film_id, description)
        assert response.json()["id"] == film_id
        assert response.json()["description"] == description["description"]