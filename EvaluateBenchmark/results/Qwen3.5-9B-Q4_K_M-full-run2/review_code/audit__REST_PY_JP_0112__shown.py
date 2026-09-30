import requests

def solve(inputs):
    url = "https://jsonplaceholder.typicode.com/users"
    payload = {
        "name": inputs["new_name"],
        "username": inputs["new_username"]
    }
    response = requests.post(url, json=payload)
    if response.status_code != 201:
        raise Exception(f"Failed to create user: HTTP {response.status_code}")
    data = response.json()
    return data.get("id")