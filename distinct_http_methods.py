import requests

response_for_invalid_get_request = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f"HTTP request without method parameter, result: {response_for_invalid_get_request.text}")

payload_head = {"method": "HEAD"}
response_head = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload_head)
print(f"HEAD request, result: {response_head.text}")

payload_post = {"method": "POST"}
response_post = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=payload_post)
print(f"Valid method parameter, POST request, result: {response_post.text}")


request_parameters = [{"method": "DELETE"}, {"method": "POST"}, {"method": "GET"}, {"method": "PUT"}]

for parameter in request_parameters:
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=parameter)
    print(f"GET method, parameter: {parameter}, result: {response.text}")

    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=parameter)
    print(f"POST method, parameter: {parameter}, result: {response.text}")

    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=parameter)
    print(f"PUT method, parameter: {parameter}, result: {response.text}")

    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", params=parameter)
    print(f"DELETE method, parameter: {parameter}, result: {response.text}")
