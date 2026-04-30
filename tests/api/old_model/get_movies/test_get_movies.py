from conftest import admin_user

class TestGetMovies:

    def test_get_movies_positive(self, api_manager, admin_user):
        response = api_manager.movies_api.get_movies(
            pageSize=10,
            page=1,
            minPrice=1,
            maxPrice=1000,
            locations="MSK",
            published="true",
            genreId=1,
            createdAt="desc"
        )
        assert response.status_code == 200

    def test_get_movies_check_filter(self, api_manager, admin_user):
        response = api_manager.movies_api.get_movies(
            pageSize=10,
            page=1,
            minPrice=1,
            maxPrice=100,
            locations="MSK",
            published="true",
            genreId=1,
            createdAt="desc"
        )

        movies = response.json()["movies"]
        assert len(movies) > 0, "Список фильмов пуст"

        for movie in movies:
            assert movie["price"] <= 100, f"Фильм {movie['id']} имеет цену {movie['price']}, ожидалось <= 100"
            assert movie["location"] == "MSK", f"Фильм {movie['id']} имеет локацию {movie['location']}, ожидалось MSK"
            assert movie["published"] is True, f"Фильм {movie['id']} не опубликован"
            assert movie["genreId"] == 1, f"Фильм {movie['id']} имеет genreId {movie['genreId']}, ожидалось 1"


