import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts", params={"userId": "not-an-integer"}, timeout=10)
print(response.json()[0]["title"])
