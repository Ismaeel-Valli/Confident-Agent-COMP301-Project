import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    url = f"https://dummyjson.com/users/{resource_id}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}")
    data = response.json()
    return None if data.get("users") == [] else data["user"]