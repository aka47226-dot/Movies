
from faker import Faker
import pytest
import requests

from api.api_manager import ApiManager
from constants import BASE_URL, REGISTER_ENDPOINT, LOGIN_ENDPOINT, LOGIN, PASSWORD
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator

faker = Faker()

@pytest.fixture(scope="session")
def admin_user():
    """
    Admin для тестов.
    """

    return {
        "email": LOGIN,
        "password": PASSWORD
    }
# conftest.py
@pytest.fixture(scope="session")
def custom_movie():
    """Фабрика для создания произвольного тела фильма."""
    def _make_movie(
        name="Default Movie",
        imageUrl=None,
        price=100,
        description="Test",
        location="MSK",
        published=True,
        genreId=1
    ):
        return {
            "name": name,
            "imageUrl": imageUrl,
            "price": price,
            "description": description,
            "location": location,
            "published": published,
            "genreId": genreId
        }
    return _make_movie

# conftest.py
@pytest.fixture()
def rand_movie():
    def _make():
        return {
            "name": faker.name(),
            "imageUrl": faker.url(),
            "price": faker.random_int(100, 500),
            "description": faker.sentence(),
            "location": "SPB",
            "published": True,
            "genreId": faker.random_int(1, 7)
        }
    return _make

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)
