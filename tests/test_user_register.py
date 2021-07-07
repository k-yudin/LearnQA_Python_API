import requests
import pytest
from datetime import datetime
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserRegister(BaseCase):
    email = ''
    def setup(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("$m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected content received: {response.content}"

    def test_create_user_with_invalid_email(self):
        email = 'vinkotovexample.com'
        data = {
            'password': 'valid_pass',
            'username': 'learnqa_valid',
            'firstName': 'learnqa_valid',
            'lastName': 'learnqa_valid',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Unexpected content received: {response.content}"

    test_data = [
        ({'password': 'valid_pass', 'firstName': 'valid_first_name', 'lastName': 'learnqa_valid', 'email': email}),
        ({'username': 'valid_username', 'firstName': 'valid_first_name', 'lastName': 'learnqa_valid', 'email': email}),
        ({'username': 'valid_username', 'password': 'valid_pass', 'lastName': 'learnqa_valid', 'email': email}),
        ({'username': 'valid_username', 'password': 'valid_pass', 'firstName': 'valid_first_name', 'email': email}),
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
            'email': self.email
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
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")
