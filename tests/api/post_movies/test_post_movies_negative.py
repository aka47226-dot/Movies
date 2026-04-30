class TestPostMoviesNegative:

    def test_post_movies_with_empty_name(self, api_manager, custom_movie):
        api_manager.auth_api.authenticate()
        response = api_manager.movies_api.post_movies(custom_movie("", "http://youtube.com/arthas", 54, "Kingdom come 2", "SPB", True, 1), expected_status = 400)

        assert response.json()["message"] == ['name should not be empty']

    def test_post_movies_with_empty_location(self, api_manager, custom_movie):
        api_manager.auth_api.authenticate()
        response = api_manager.movies_api.post_movies(custom_movie("Stream papicha", "http://youtube.com/arthas", 54, "Kingdom come 2", "", True, 1), expected_status = 400)

        assert response.json()["message"] == ['Поле location должно быть одним из: MSK, SPB']