import requests

class TestCookie:
    def test_cookie(self):
        url = "https://playground.learnqa.ru/api/homework_cookie"
        response = requests.get(url)

        expected_response_parameter = 'HomeWork'

        actual_response_cookie_value = response.cookies.get(expected_response_parameter)
        expected_response_cookie_value = 'hw_value'

        assert expected_response_parameter in response.cookies, F"There is no cookie {expected_response_parameter} in the response"
        assert actual_response_cookie_value == expected_response_cookie_value, f"Cookie has invalid value, actual value is: {actual_response_cookie_value}"
