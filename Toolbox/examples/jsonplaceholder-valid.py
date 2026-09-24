import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=10)
response.raise_for_status()
data = response.json()
print(data["title"])
