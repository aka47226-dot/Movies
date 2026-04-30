from conftest import admin_user


class TestMoviesNegative:

    #GET /movies

    def test_get_movies_invalid_location(self, api_manager, admin_user):
        response = api_manager.movies_api.get_movies(
            expected_status=400,
            pageSize=10,
            page=1,
            minPrice=1,
            maxPrice=1000,
            locations="NSK",
            published="true",
            genreId=1,
            createdAt="desc"
        )
        assert response.json()["message"] == "Некорректные данные"

    def test_get_movies_invalid_group_by(self, api_manager, admin_user):
        response = api_manager.movies_api.get_movies(
            expected_status=400,
            pageSize=10,
            page=1,
            minPrice=1,
            maxPrice=1000,
            locations="NSK",
            published="true",
            genreId=1,
            createdAt="dsc"
        )
        assert response.json()["message"] == "Некорректные данные"

    #GET /movies/{id}

    def test_get_movies_id_invalid_id(self, api_manager, rand_movie):
        api_manager.auth_api.authenticate()

        response = api_manager.movies_api.post_movies(rand_movie())
        film_id = response.json().get("id")

        api_manager.movies_api.delete_movie_with_id(film_id)

        response = api_manager.movies_api.get_movie_with_id(film_id, expected_status=404)
        assert response.json()["message"] == "Фильм не найден"

    #POST /movies

    def test_post_movies_with_empty_name(self, api_manager, custom_movie):
        api_manager.auth_api.authenticate()
        response = api_manager.movies_api.post_movies(
            custom_movie("", "http://youtube.com/arthas", 54, "Kingdom come 2", "SPB", True, 1),
            expected_status=400
        )
        assert response.json()["message"] == ['name should not be empty']

    def test_post_movies_with_empty_location(self, api_manager, custom_movie):
        api_manager.auth_api.authenticate()
        response = api_manager.movies_api.post_movies(
            custom_movie("Stream papicha", "http://youtube.com/arthas", 54, "Kingdom come 2", "", True, 1),
            expected_status=400
        )
        assert response.json()["message"] == ['Поле location должно быть одним из: MSK, SPB']

    #PATCH /movies/{id}

    def test_patch_movie_invalid_field(self, api_manager, rand_movie):
        api_manager.auth_api.authenticate()
        response = api_manager.movies_api.post_movies(rand_movie())

        data = response.json()
        film_id = data["id"]

        invalid_value = {"value": "Patched"}

        api_manager.movies_api.patch_movie_with_id(film_id, invalid_value, expected_status=404)

    #DELETE /movies/{id}

    def test_delete_movies_with_invalid_id(self, api_manager, rand_movie):
        api_manager.auth_api.authenticate()

        response = api_manager.movies_api.post_movies(rand_movie())
        film_id = response.json().get("id")

        api_manager.movies_api.delete_movie_with_id(film_id)

        response = api_manager.movies_api.delete_movie_with_id(film_id, expected_status=404)
        assert response.json()["message"] == "Фильм не найден"