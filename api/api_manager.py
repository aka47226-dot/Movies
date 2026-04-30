from clients.movies_api import MoviesAPI
from clients.auth_api import AuthApi


class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.movies_api = MoviesAPI(session)
        self.auth_api = AuthApi(session)
