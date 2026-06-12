from venv import logger

import allure
import pytest

from conftest import admin_user, common_user, test_user
from models.user import User


@allure.epic("Тестирование фильмов")
@allure.feature("API тестирование эндпоинтов фильмов")
class TestMovies:

    # ================================================================= GET /movies

    @allure.story("Получение списка фильмов")
    @allure.title("Позитивный тест получения списка фильмов")
    @allure.description("""
    Тест проверяет успешное получение списка фильмов с валидными фильтрами.
    Шаги:
    1. Выполнить GET /movies с валидными параметрами.
    2. Проверить, что статус ответа 200.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_movies_positive(self, api_manager, admin_user):
        with allure.step("Выполняем GET /movies с валидными параметрами"):
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
        with allure.step("Проверяем, что статус ответа 200"):
            assert response.status_code == 200

    @pytest.mark.slow
    @allure.story("Получение списка фильмов с проверкой фильтров")
    @allure.title("Тест корректности применения фильтров при получении фильмов")
    @allure.description("""
    Тест проверяет, что все возвращённые фильмы соответствуют переданным фильтрам.
    Шаги:
    1. Выполнить GET /movies с параметрами фильтрации (maxPrice=100, MSK, genreId=1).
    2. Проверить, что список фильмов не пуст.
    3. Проверить каждый фильм на соответствие заданным фильтрам.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_check_filter(self, api_manager, admin_user):
        with allure.step("Выполняем GET /movies с параметрами фильтрации"):
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

        with allure.step("Проверяем, что список фильмов не пуст"):
            movies = response.json()["movies"]
            assert len(movies) > 0, "Список фильмов пуст"

        with allure.step("Проверяем каждый фильм на соответствие фильтрам"):
            for movie in movies:
                assert movie["price"] <= 100, \
                    f"Фильм {movie['id']} имеет цену {movie['price']}, ожидалось <= 100"
                assert movie["location"] == "MSK", \
                    f"Фильм {movie['id']} имеет локацию {movie['location']}, ожидалось MSK"
                assert movie["published"] is True, \
                    f"Фильм {movie['id']} не опубликован"
                assert movie["genreId"] == 1, \
                    f"Фильм {movie['id']} имеет genreId {movie['genreId']}, ожидалось 1"

    # ================================================================= POST /movies

    @allure.story("Создание фильма")
    @allure.title("Позитивный тест создания фильма")
    @allure.description("""
    Тест проверяет успешное создание фильма через POST /movies.
    Шаги:
    1. Авторизация под администратором.
    2. Создание фильма с рандомными данными.
    3. Проверка полей созданного фильма в ответе.
    4. Получение фильма по id и повторная проверка данных.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_post_movies(self, api_manager, rand_movie):
        with allure.step("Авторизация"):
            api_manager.auth_api.authenticate()

        with allure.step("Создаём фильм с рандомными данными"):
            movie = rand_movie()
            response = api_manager.movies_api.post_movies(movie)

        with allure.step("Проверяем поля фильма в ответе на POST"):
            data = response.json()
            assert data["name"] == movie["name"]
            assert data["price"] == movie["price"]
            assert data["description"] == movie["description"]

        with allure.step("Получаем фильм по id и проверяем данные"):
            response = api_manager.movies_api.get_movie_with_id(data["id"])
            data = response.json()
            assert data["name"] == movie["name"]
            assert data["price"] == movie["price"]
            assert data["description"] == movie["description"]

    # ================================================================= PATCH /movies/{id}

    @allure.story("Обновление фильма")
    @allure.title("Позитивный тест полного обновления фильма")
    @allure.description("""
    Тест проверяет успешное обновление данных фильма через PATCH /movies/{id}.
    Шаги:
    1. Авторизация.
    2. Создание фильма.
    3. Обновление фильма новыми данными.
    4. Проверка id и нового name в ответе.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_patch_movie(self, api_manager, rand_movie):
        with allure.step("Авторизация"):
            api_manager.auth_api.authenticate()

        with allure.step("Создаём фильм"):
            response = api_manager.movies_api.post_movies(rand_movie())
            data = response.json()
            film_id = data["id"]

        with allure.step("Обновляем фильм новыми рандомными данными"):
            rand_movie = rand_movie()
            response = api_manager.movies_api.patch_movie_with_id(film_id, rand_movie)

        with allure.step("Проверяем id и обновлённое name"):
            assert response.json()["id"] == film_id
            assert response.json()["name"] == rand_movie["name"]

    @allure.story("Обновление фильма")
    @allure.title("Тест частичного обновления — изменение описания фильма")
    @allure.description("""
    Тест проверяет успешное обновление только поля description через PATCH /movies/{id}.
    Шаги:
    1. Авторизация.
    2. Создание фильма.
    3. Обновление только поля description.
    4. Проверка id и нового description в ответе.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_patch_movie_description(self, api_manager, rand_movie):
        with allure.step("Авторизация"):
            api_manager.auth_api.authenticate()

        with allure.step("Создаём фильм"):
            response = api_manager.movies_api.post_movies(rand_movie())
            data = response.json()
            film_id = data["id"]

        with allure.step("Обновляем только поле description"):
            description = {"description": "Patched"}
            response = api_manager.movies_api.patch_movie_with_id(film_id, description)

        with allure.step("Проверяем id и обновлённое description"):
            assert response.json()["id"] == film_id
            assert response.json()["description"] == description["description"]

    # ================================================================= DELETE /movies/{id}

    @allure.story("Удаление фильма")
    @allure.title("Позитивный тест удаления фильма")
    @allure.description("""
    Тест проверяет успешное удаление фильма через DELETE /movies/{id}.
    Шаги:
    1. Авторизация.
    2. Создание фильма.
    3. Удаление фильма.
    4. Проверка, что фильм не найден (статус 404).
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_movies(self, api_manager, rand_movie):
        with allure.step("Авторизация"):
            api_manager.auth_api.authenticate()

        with allure.step("Создаём фильм"):
            response = api_manager.movies_api.post_movies(rand_movie())
            film_id = response.json().get("id")

        with allure.step("Удаляем фильм"):
            api_manager.movies_api.delete_movie_with_id(film_id)

        with allure.step("Проверяем, что фильм не найден после удаления (404)"):
            response = api_manager.movies_api.get_movie_with_id(film_id, expected_status=404)
            assert response.json()["message"] == "Фильм не найден"

    # ================================================================= NEGATIVE GET /movies

    @allure.story("Получение списка фильмов с невалидными данными")
    @allure.title("Негативный тест — невалидная локация в фильтре")
    @allure.description("""
    Тест проверяет обработку невалидного значения локации (NSK) при запросе фильмов.
    Шаги:
    1. Выполнить GET /movies с locations=NSK.
    2. Проверить, что статус ответа 400.
    3. Проверить текст сообщения об ошибке.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_invalid_location(self, api_manager, admin_user):
        with allure.step("Выполняем GET /movies с невалидной локацией NSK"):
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
        with allure.step("Проверяем сообщение об ошибке"):
            assert response.json()["message"] == ['Каждое значение в поле locations должно быть одним из значений: MSK, SPB']

    @pytest.mark.slow
    @allure.story("Получение списка фильмов с невалидными данными")
    @allure.title("Негативный тест — невалидное значение сортировки")
    @allure.description("""
    Тест проверяет обработку невалидного значения параметра createdAt (dsc вместо desc).
    Шаги:
    1. Выполнить GET /movies с createdAt=dsc.
    2. Проверить, что статус ответа 400.
    3. Проверить текст сообщения об ошибке.
    """)
    @allure.severity(allure.severity_level.MINOR)
    def test_get_movies_invalid_group_by(self, api_manager, admin_user):
        with allure.step("Выполняем GET /movies с невалидным значением сортировки dsc"):
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
        with allure.step("Проверяем сообщение об ошибке"):
            assert response.json()["message"] == ['Каждое значение в поле locations должно быть одним из значений: MSK, SPB']

    # ================================================================= NEGATIVE GET /movies/{id}

    @allure.story("Получение фильма по несуществующему id")
    @allure.title("Негативный тест — запрос удалённого фильма по id")
    @allure.description("""
    Тест проверяет, что запрос удалённого фильма возвращает 404.
    Шаги:
    1. Авторизация.
    2. Создание фильма.
    3. Удаление фильма.
    4. Запрос фильма по удалённому id.
    5. Проверка статуса 404 и текста ошибки.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_id_invalid_id(self, api_manager, rand_movie):
        with allure.step("Авторизация"):
            api_manager.auth_api.authenticate()

        with allure.step("Создаём фильм"):
            response = api_manager.movies_api.post_movies(rand_movie())
            film_id = response.json().get("id")

        with allure.step("Удаляем фильм"):
            api_manager.movies_api.delete_movie_with_id(film_id)

        with allure.step("Запрашиваем удалённый фильм и проверяем ошибку 404"):
            response = api_manager.movies_api.get_movie_with_id(film_id, expected_status=404)
            assert response.json()["message"] == "Фильм не найден"

    # ================================================================= NEGATIVE POST /movies

    @allure.story("Создание фильма с невалидными данными")
    @allure.title("Негативный тест — создание фильма с пустым названием")
    @allure.description("""
    Тест проверяет, что создание фильма с пустым полем name возвращает 400.
    Шаги:
    1. Авторизация.
    2. Попытка создания фильма с name="".
    3. Проверка статуса 400 и текста ошибки.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_post_movies_with_empty_name(self, api_manager, custom_movie):
        with allure.step("Авторизация"):
            api_manager.auth_api.authenticate()

        with allure.step("Пытаемся создать фильм с пустым name"):
            response = api_manager.movies_api.post_movies(
                custom_movie("", "http://youtube.com/arthas", 54, "Kingdom come 2", "SPB", True, 1),
                expected_status=400
            )

        with allure.step("Проверяем сообщение об ошибке"):
            assert response.json()["message"] == ["Поле name не может быть пустым"] or ["Поле name должно содержать не менее 3 символов"]

    @allure.story("Создание фильма с невалидными данными")
    @allure.title("Негативный тест — создание фильма с пустой локацией")
    @allure.description("""
    Тест проверяет, что создание фильма с пустым полем location возвращает 400.
    Шаги:
    1. Авторизация.
    2. Попытка создания фильма с location="".
    3. Проверка статуса 400 и текста ошибки.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_post_movies_with_empty_location(self, api_manager, custom_movie):
        with allure.step("Авторизация"):
            api_manager.auth_api.authenticate()

        with allure.step("Пытаемся создать фильм с пустой location"):
            response = api_manager.movies_api.post_movies(
                custom_movie("Stream papicha", "http://youtube.com/arthas", 54, "Kingdom come 2", "", True, 1),
                expected_status=400
            )

        with allure.step("Проверяем сообщение об ошибке"):
            assert response.json()["message"] == [
                "Поле location должно быть одним из: MSK, SPB",
                "Поле location не может быть пустым"
            ]

    # ================================================================= NEGATIVE PATCH /movies/{id}

    @allure.story("Обновление фильма с невалидными данными")
    @allure.title("Негативный тест — обновление фильма с несуществующим полем")
    @allure.description("""
    Тест проверяет, что PATCH с невалидным полем возвращает 400.
    Шаги:
    1. Авторизация.
    2. Создание фильма.
    3. Попытка обновления с телом {"value": "Patched"}.
    4. Проверка статуса 400.
    """)
    @allure.severity(allure.severity_level.MINOR)
    def test_patch_movie_invalid_field(self, api_manager, rand_movie):
        with allure.step("Авторизация"):
            api_manager.auth_api.authenticate()

        with allure.step("Создаём фильм"):
            response = api_manager.movies_api.post_movies(rand_movie())
            data = response.json()
            film_id = data["id"]

        with allure.step("Пытаемся обновить фильм с невалидным полем value"):
            invalid_value = {"value": "Patched"}
            api_manager.movies_api.patch_movie_with_id(film_id, invalid_value, expected_status=400)

    @allure.story("Валидация модели пользователя")
    @allure.title("Тест валидации данных регистрации пользователя")
    @allure.description("""
    Тест проверяет, что данные регистрации пользователя проходят валидацию модели User.
    Шаги:
    1. Передать registration_user_data в User.model_validate.
    2. Проверить, что email не равен None.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_registration_user_valid(self, registration_user_data):
        with allure.step("Валидируем данные регистрации"):
            user = User.model_validate(registration_user_data)

        with allure.step("Проверяем, что email не None"):
            assert user.email is not None

    # ================================================================= NEGATIVE DELETE /movies/{id}

    @allure.story("Удаление фильма с невалидными данными")
    @allure.title("Негативный тест — повторное удаление уже удалённого фильма")
    @allure.description("""
    Тест проверяет, что попытка удалить уже удалённый фильм возвращает 404.
    Шаги:
    1. Авторизация.
    2. Создание фильма.
    3. Удаление фильма.
    4. Повторная попытка удаления того же фильма.
    5. Проверка статуса 404 и текста ошибки.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_movies_with_invalid_id(self, api_manager, rand_movie):
        with allure.step("Авторизация"):
            api_manager.auth_api.authenticate()

        with allure.step("Создаём фильм"):
            response = api_manager.movies_api.post_movies(rand_movie())
            film_id = response.json().get("id")

        with allure.step("Удаляем фильм"):
            api_manager.movies_api.delete_movie_with_id(film_id)

        with allure.step("Повторно пытаемся удалить тот же фильм"):
            response = api_manager.movies_api.delete_movie_with_id(film_id, expected_status=404)
            assert response.json()["message"] == "Фильм не найден"

    # ================================================================= NEW

    @allure.story("Ролевой доступ — создание фильма")
    @allure.title("Негативный тест — создание фильма пользователем с ролью common_user")
    @allure.description("""
    Тест проверяет, что пользователь с ролью common_user не может создавать фильмы.
    Шаги:
    1. Авторизация под common_user.
    2. Попытка создания фильма.
    3. Проверка статуса 403 и сообщения Forbidden resource.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_movies_with_user_role(self, api_manager, rand_movie, common_user):
        with allure.step("Авторизуемся под common_user"):
            api_manager.auth_api.authenticate(common_user.creds)

        with allure.step("Пытаемся создать фильм"):
            response = api_manager.movies_api.post_movies(rand_movie(), expected_status=403)

        with allure.step("Проверяем ошибку доступа 403 Forbidden resource"):
            assert response.json()["message"] == "Forbidden resource"

    @pytest.mark.parametrize("minprice, maxprice, location, genreid", [
        (1, 100, "MSK", 1),
        (100, 1000, "SPB", 5)
    ])
    @allure.story("Параметризованная проверка фильтрации фильмов")
    @allure.title("Тест фильтрации фильмов с параметризованными значениями")
    @allure.description("""
    Тест проверяет корректность фильтрации фильмов для разных наборов параметров.
    Шаги:
    1. Выполнить GET /movies с заданными параметрами.
    2. Проверить, что список фильмов не пуст.
    3. Проверить каждый фильм на соответствие переданным фильтрам.
    """)
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_movies_check_filter_parametrized(self, api_manager, admin_user, minprice, maxprice, location, genreid):
        with allure.step(f"Выполняем GET /movies (maxPrice={maxprice}, location={location}, genreId={genreid})"):
            response = api_manager.movies_api.get_movies(
                pageSize=10,
                page=1,
                minPrice=minprice,
                maxPrice=maxprice,
                locations=location,
                published="true",
                genreId=genreid,
                createdAt="desc"
            )

        with allure.step("Проверяем, что список фильмов не пуст"):
            movies = response.json()["movies"]
            assert len(movies) > 0, "Список фильмов пуст"

        with allure.step("Проверяем каждый фильм на соответствие фильтрам"):
            for movie in movies:
                assert movie["price"] <= maxprice, \
                    f"Фильм {movie['id']} имеет цену {movie['price']}, ожидалось <= {maxprice}"
                assert movie["location"] == location, \
                    f"Фильм {movie['id']} имеет локацию {movie['location']}, ожидалось {location}"
                assert movie["published"] is True, \
                    f"Фильм {movie['id']} не опубликован"
                assert movie["genreId"] == genreid, \
                    f"Фильм {movie['id']} имеет genreId {movie['genreId']}, ожидалось {genreid}"

    @pytest.mark.slow
    @pytest.mark.parametrize("user", ["admin_user", "common_user"], indirect=True)
    @allure.story("Ролевой доступ — удаление фильма")
    @allure.title("Негативный тест — удаление фильма пользователями без прав")
    @allure.description("""
    Тест проверяет, что пользователи с ролями admin_user и common_user не могут удалять фильмы.
    Шаги:
    1. Авторизация под администратором.
    2. Создание фильма.
    3. Авторизация под тестируемым пользователем.
    4. Попытка удалить фильм.
    5. Проверка статуса 403 и сообщения Forbidden resource.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_movies_with_invalid_role(self, api_manager, rand_movie, user):
        with allure.step("Авторизуемся под администратором"):
            api_manager.auth_api.authenticate()

        with allure.step("Создаём фильм"):
            response = api_manager.movies_api.post_movies(rand_movie())
            film_id = response.json().get("id")

        with allure.step("Авторизуемся под тестируемым пользователем"):
            api_manager.auth_api.authenticate(user.creds)

        with allure.step("Пытаемся удалить фильм"):
            response = api_manager.movies_api.delete_movie_with_id(film_id, expected_status=403)

        with allure.step("Проверяем ошибку доступа 403 Forbidden resource"):
            assert response.json()["message"] == "Forbidden resource"