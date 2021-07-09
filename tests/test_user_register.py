import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):
    def test_create_user(self):
        data = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected content received: {response.content}"

    def test_create_user_with_invalid_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected content received: {response.content}"

    test_data = [
        ({'password': 'valid_pass', 'firstName': 'valid_first_name', 'lastName': 'learnqa_valid', 'email': 'some_valid@mail.com'}),
        ({'username': 'valid_username', 'firstName': 'valid_first_name', 'lastName': 'learnqa_valid', 'email': 'some_valid_2@mail.com'}),
        ({'username': 'valid_username', 'password': 'valid_pass', 'lastName': 'learnqa_valid', 'email': 'some_valid_3@mail.com'}),
        ({'username': 'valid_username', 'password': 'valid_pass', 'firstName': 'valid_first_name', 'email': 'some_valid_4@mail.com'}),
        ({'username': 'valid_username', 'password': 'valid_pass', 'firstName': 'valid_first_name', 'lastName': 'learnqa_valid'})
    ]

    @pytest.mark.parametrize("data", test_data)
    def test_create_user_without_username_required_field(self, data):
        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        print(response.content.decode("utf-8"))

    def test_create_user_with_short_username(self):
        data = {
            'username': 'valid_username',
            'password': 'valid_pass',
            'firstName': 'A',
            'lastName': 'learnqa_valid',
            'email': self.generate_unique_email()
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'firstName' field is too short", f"Unexpected content received: {response.content}"

    def test_create_user_with_long_username(self):
        data = {
            'username': 'valid_username',
            'password': 'valid_pass',
            'firstName': 'D2c0DYJ5eaBiH54EDnS67ryOWBoj7qIfwLNEKUpccltGT1IdGbwAw1icys29VKdUkpJpqLYUYsNwSPInO15j7LtwUX5BSgEaTrqhPlwyHOItAlHcjAHdsArFYfO9p6iB0ThDFih3nQXO88v7ZXvsRHauUmT3DAbwsROEA9aVEggED8R4BxZx0d97BEOuGgdRXSHksLgtmSPFnuCYLvGJxATXorLd4AMnI89kWswfV84iYgRAYZCTsRky02i',
            'lastName': 'learnqa_valid',
            'email': self.generate_unique_email()
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")
