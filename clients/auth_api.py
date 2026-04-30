from constants import LOGIN, PASSWORD, BASE_URL, AUTH_URL, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class AuthApi(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_URL)

    def authenticate(self):
        login_data = {
            "email": LOGIN,
            "password": PASSWORD
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self._update_session_headers(**{"authorization": "Bearer " + token})

    def login_user(self, login_data, expected_status=200):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )