from constants.constants import LOGIN, PASSWORD, AUTH_URL, LOGIN_ENDPOINT, REGISTER_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class AuthApi(CustomRequester):

    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_URL)

    def register_user(self, user_data: dict, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def authenticate(self, creds=None):
        login_data = {
            "email": creds[0] if creds else LOGIN,
            "password": creds[1] if creds else PASSWORD
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