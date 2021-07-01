import requests

class TestHeaders:
    def test_headers(self):
        url = "https://playground.learnqa.ru/api/homework_header"
        response = requests.get(url)

        expected_response_parameter = 'x-secret-homework-header'

        actual_response_header_value = response.headers[expected_response_parameter]
        expected_response_header_value = 'Some secret value'

        assert expected_response_parameter in response.headers, f"There is no header parameter {expected_response_parameter} in the response"
        assert actual_response_header_value == expected_response_header_value, f"Header parameter has invalid value, actual value is: {actual_response_header_value}"
