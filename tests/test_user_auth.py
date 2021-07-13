import pytest
import allure
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response, "auth_sid")
        self.token = self.get_header(response, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response, "user_id")

    @allure.description("Test for successful authorization using email and password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_auth_user(self):
        second_response = MyRequests.get(
            "/user/auth",
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            second_response,
            "user_id",
            self.user_id_from_auth_method,
            "user_id from auth method is not equal to user_id from check method")

    @allure.description("Test for authorization status w/o auth cookie or token")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        if condition == "no_cookie":
            second_response = MyRequests.get(
                "/user/auth",
                headers={"x-csrf-token": self.token})
        else:
            second_response = MyRequests.get(
                "/user/auth",
                cookies={"auth_sid": self.auth_sid})

        Assertions.assert_json_value_by_name(
            second_response,
            "user_id",
            0,
            f"User is authorized with condition: {condition}"
        )