import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Delete users cases")
class TestUserDelete(BaseCase):

    @allure.description("Test tries to delete user from the group that is not allowed to de done")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_user_from_restricted_group(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        user_id = self.get_json_value(response, "user_id")

        delete_response = MyRequests.delete(f"/user/{user_id}",
                                          headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid}
                                          )

        Assertions.assert_code_status(delete_response, 400)

        assert delete_response.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.",\
            f"Unexpected content received: {delete_response.content}"

    @allure.description("Test for successful user delete")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_successfully(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response = MyRequests.post("/user/", data=register_data)

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

        login_response = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(login_response, "auth_sid")
        token = self.get_header(login_response, "x-csrf-token")

        # DELETE
        delete_response = MyRequests.delete(f"/user/{user_id}",
                                          headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid}
                                          )

        Assertions.assert_code_status(delete_response, 200)

        # GET
        get_response = MyRequests.get(f"/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(get_response, 404)
        assert get_response.content.decode("utf-8") == "User not found",\
            f"Unexpected content received: {get_response.content}"

    @allure.description("Test that tries to delete user being authorized as other user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("Security")
    def test_delete_user_as_other_user(self):
        # REGISTER FIRST USER
        register_data_first_user = self.prepare_registration_data()
        response_first_user = MyRequests.post("/user/", data=register_data_first_user)

        Assertions.assert_code_status(response_first_user, 200)
        Assertions.assert_json_has_key(response_first_user, "id")

        first_user_id = self.get_json_value(response_first_user, "id")

        # REGISTER SECOND USER
        register_data_second_user = self.prepare_registration_data()
        response_second_user = MyRequests.post("/user/", data=register_data_second_user)

        Assertions.assert_code_status(response_second_user, 200)
        Assertions.assert_json_has_key(response_second_user, "id")

        email_second_user = register_data_second_user['email']
        password_second_user = register_data_second_user['password']

        # SECOND USER LOGIN
        login_data_second_user = {
            'email': email_second_user,
            'password': password_second_user
        }

        login_response_second_user = MyRequests.post("/user/login",
                                                   data=login_data_second_user)

        auth_sid_second_user = self.get_cookie(login_response_second_user, "auth_sid")
        token_second_user = self.get_header(login_response_second_user, "x-csrf-token")

        # DELETE FIRST USER
        MyRequests.delete(f"/user/{first_user_id}",
                                          headers={"x-csrf-token": token_second_user},
                                          cookies={"auth_sid": auth_sid_second_user}
                                          )

        # GET FIRST USER
        get_response = MyRequests.get(f"/user/{first_user_id}")

        Assertions.assert_code_status(get_response, 200)
