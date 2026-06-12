import allure

from conftest import created_test_user


class TestDBMovies:

    @allure.story("Создание фильма и проверка его наличия в БД")
    @allure.title("Позитивный тест")
    @allure.description("""
        Тест проверяет, что фильм создается в БД
        """)
    @allure.severity(allure.severity_level.NORMAL)

    def test_db_movies(self, api_manager, rand_movie, db_helper, created_test_user):
        api_manager.auth_api.authenticate()
        movie = rand_movie()

        assert db_helper.get_movie_by_name(movie["name"]) is None
        
        response = api_manager.movies_api.post_movies(movie)

        data = response.json()
        assert data["name"] == movie["name"]
        assert data["price"] == movie["price"]
        assert data["description"] == movie["description"]

        assert db_helper.get_movie_by_name(movie["name"]) is not None

        api_manager.movies_api.delete_movie_with_id(data["id"])

        assert db_helper.get_movie_by_name(movie["name"]) is None