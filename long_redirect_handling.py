import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
all_responses = response.history
print(f"Count of redirects: {len(all_responses)}")
print(f"Final destination URL: {response.url}")
