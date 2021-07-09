import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data['email']
        user_id = self.get_json_value(response, "id")
        password = register_data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        login_response = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(login_response, "auth_sid")
        token = self.get_header(login_response, "x-csrf-token")

        # EDIT
        new_name = "Changed name"
        edit_response = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid},
                                     data={"firstName": new_name})

        Assertions.assert_code_status(edit_response, 200)

        # GET
        get_response = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(get_response,
                                             "firstName",
                                             new_name,
                                             "Wrong name of the user after edit")


    def test_edit_user_no_auth(self):
        register_data = self.prepare_registration_data()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")

        new_name = "Updated name"
        edit_response = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                         headers={"x-csrf-token": "any_token"},
                                         cookies={"auth_sid": "any_session_id"},
                                         data={"firstName": new_name})

        Assertions.assert_code_status(edit_response, 400)

    @pytest.mark.xfail(reason="Security issue, user can edit data of other users without being authenticated, issue is reported in ticket #1717")
    def test_edit_user_as_other_user(self):
        # REGISTER FIRST USER
        register_data_first_user = self.prepare_registration_data()
        response_first_user = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_first_user)

        Assertions.assert_code_status(response_first_user, 200)
        Assertions.assert_json_has_key(response_first_user, "id")

        first_user_id = self.get_json_value(response_first_user, "id")

        # REGISTER SECOND USER
        register_data_second_user = self.prepare_registration_data()
        response_second_user = requests.post("https://playground.learnqa.ru/api/user/", data=register_data_second_user)

        Assertions.assert_code_status(response_second_user, 200)
        Assertions.assert_json_has_key(response_second_user, "id")

        email_second_user = register_data_second_user['email']
        password_second_user = register_data_second_user['password']

        # SECOND USER LOGIN
        login_data_second_user = {
            'email': email_second_user,
            'password': password_second_user
        }

        login_response_second_user = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data_second_user)

        auth_sid_second_user = self.get_cookie(login_response_second_user, "auth_sid")
        token_second_user = self.get_header(login_response_second_user, "x-csrf-token")

        # EDIT FIRST USER
        new_name = "Edited name"
        edit_response = requests.put(f"https://playground.learnqa.ru/api/user/{first_user_id}",
                                     headers={"x-csrf-token": token_second_user},
                                     cookies={"auth_sid": auth_sid_second_user},
                                     data={"firstName": new_name})

        assert edit_response.status_code == 400,\
            f"User can edit data as logged in as other user"

    def test_edit_user_invalid_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data['email']
        user_id = self.get_json_value(response, "id")
        password = register_data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        login_response = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(login_response, "auth_sid")
        token = self.get_header(login_response, "x-csrf-token")

        # EDIT
        invalid_email = "somemail.com"
        edit_response = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                         headers={"x-csrf-token": token},
                                         cookies={"auth_sid": auth_sid},
                                         data={"email": invalid_email})

        Assertions.assert_code_status(edit_response, 400)
        assert edit_response.content.decode("utf-8") == "Invalid email format",\
            f"Unexpected content received: {response.content}"

    def test_edit_user_short_name(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response = requests.post("https://playground.learnqa.ru/api/user/", data=register_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        email = register_data['email']
        user_id = self.get_json_value(response, "id")
        password = register_data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        login_response = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(login_response, "auth_sid")
        token = self.get_header(login_response, "x-csrf-token")

        # EDIT
        new_name = "B"
        edit_response = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                                         headers={"x-csrf-token": token},
                                         cookies={"auth_sid": auth_sid},
                                         data={"firstName": new_name})

        # GET
        get_response = requests.get(f"https://playground.learnqa.ru/api/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(edit_response, 200)
        Assertions.assert_json_value_by_name(get_response,
                                             "firstName",
                                             new_name,
                                             "Wrong name of the user after edit")
