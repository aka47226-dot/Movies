from constants.constants import BASE_URL, MOVIES_ENDPOINT
from custom_requester.custom_requester import CustomRequester

class MoviesAPI(CustomRequester):
    """
      Класс для работы с MoviesAPI.
      """

    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL)

    def get_movies(self, expected_status=200, **query_params):
        """
        Получение списка фильмов с фильтрацией.
        """
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            params=query_params,
            expected_status=expected_status
        )

    def get_movie_with_id(self, film_id, expected_status=200):
        """
        Получение списка фильмов с фильтрацией.
        """
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES_ENDPOINT}/{film_id}",
            expected_status=expected_status
        )

    def delete_movie_with_id(self, film_id, expected_status=200):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES_ENDPOINT}/{film_id}",
            expected_status=expected_status
        )

    def patch_movie_with_id(self, film_id, movie, expected_status=200):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES_ENDPOINT}/{film_id}",
            expected_status=expected_status,
            data = movie
        )

    def post_movies(self, movie, expected_status=201):
        """
                Создание фильма.
                """
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie,
            expected_status=expected_status
        )