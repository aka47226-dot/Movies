from conftest import admin_user

class TestGetMoviesNegative:

    def test_get_movies_invalid_location(self, api_manager, admin_user):
        response = api_manager.movies_api.get_movies(expected_status = 400,
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
        response = api_manager.movies_api.get_movies(expected_status = 400,
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