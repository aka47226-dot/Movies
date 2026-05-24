from api.api_manager import ApiManager
from models.base_models import RegisterUserResponse
from models.user import User

class TestAuth:

    def test_register_user(self, api_manager: ApiManager, registration_user_data):
        user = User.model_validate(registration_user_data)
        response = api_manager.auth_api.register_user(user_data=registration_user_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == user.email, "Email не совпадает"