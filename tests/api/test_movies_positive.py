from conftest import admin_user


class TestMoviesPositive:

    # GET /movies

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

    #POST /movies

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

    #PATCH /movies/{id}

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

    #DELETE /movies/{id}

    def test_delete_movies(self, api_manager, rand_movie):
        api_manager.auth_api.authenticate()

        response = api_manager.movies_api.post_movies(rand_movie())
        film_id = response.json().get("id")

        api_manager.movies_api.delete_movie_with_id(film_id)

        response = api_manager.movies_api.get_movie_with_id(film_id, expected_status=404)
        assert response.json()["message"] == "Фильм не найден"