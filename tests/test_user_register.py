import allure
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

@allure.epic("Registration cases")
class TestUserRegister(BaseCase):

    @allure.description("Test that verifies that user was created successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("Test that tries to create user with already existing email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected content received: {response.content}"

    @allure.description("Test that tries to create user with invalid email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_invalid_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected content received: {response.content}"

    test_data = [
        ({'password': 'valid_pass', 'firstName': 'valid_first_name', 'lastName': 'learnqa_valid', 'email': 'some_valid@mail.com'}),
        ({'username': 'valid_username', 'firstName': 'valid_first_name', 'lastName': 'learnqa_valid', 'email': 'some_valid_2@mail.com'}),
        ({'username': 'valid_username', 'password': 'valid_pass', 'lastName': 'learnqa_valid', 'email': 'some_valid_3@mail.com'}),
        ({'username': 'valid_username', 'password': 'valid_pass', 'firstName': 'valid_first_name', 'email': 'some_valid_4@mail.com'}),
        ({'username': 'valid_username', 'password': 'valid_pass', 'firstName': 'valid_first_name', 'lastName': 'learnqa_valid'})
    ]

    @allure.description("Test that tries to create user w/o one of the required parameters")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("data", test_data)
    def test_create_user_without_required_field(self, data):
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        print(response.content.decode("utf-8"))

    @allure.description("Test that tries to create user with short first name parameter")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_short_first_name(self):
        data = {
            'username': 'valid_username',
            'password': 'valid_pass',
            'firstName': 'A',
            'lastName': 'learnqa_valid',
            'email': self.generate_unique_email()
        }

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'firstName' field is too short", f"Unexpected content received: {response.content}"

    @allure.description("Test that tries to create user with long first name parameter")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_long_first_name(self):
        data = {
            'username': 'valid_username',
            'password': 'valid_pass',
            'firstName': 'D2c0DYJ5eaBiH54EDnS67ryOWBoj7qIfwLNEKUpccltGT1IdGbwAw1icys29VKdUkpJpqLYUYsNwSPInO15j7LtwUX5BSgEaTrqhPlwyHOItAlHcjAHdsArFYfO9p6iB0ThDFih3nQXO88v7ZXvsRHauUmT3DAbwsROEA9aVEggED8R4BxZx0d97BEOuGgdRXSHksLgtmSPFnuCYLvGJxATXorLd4AMnI89kWswfV84iYgRAYZCTsRky02i',
            'lastName': 'learnqa_valid',
            'email': self.generate_unique_email()
        }

        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'firstName' field is too long", f"Unexpected content received: {response.content}"
