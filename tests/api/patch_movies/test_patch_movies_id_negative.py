class TestPatchMoviesIdNegative:

    def test_patch_movie_description(self, api_manager, rand_movie):
        api_manager.auth_api.authenticate()
        response = api_manager.movies_api.post_movies(rand_movie())

        data = response.json()
        film_id = data["id"]

        invalid_value = {"value": "Patched"}

        response = api_manager.movies_api.patch_movie_with_id(film_id, invalid_value, expected_status=404)