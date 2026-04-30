class TestGetMoviesIdNegative:

    def test_get_movies_id_invalid_id(self, api_manager, rand_movie):
        api_manager.auth_api.authenticate()

        response = api_manager.movies_api.post_movies(rand_movie())

        film_id = response.json().get("id")

        api_manager.movies_api.delete_movie_with_id(film_id)

        response = api_manager.movies_api.get_movie_with_id(film_id, expected_status=404)
        assert response.json()["message"] == "Фильм не найден"


