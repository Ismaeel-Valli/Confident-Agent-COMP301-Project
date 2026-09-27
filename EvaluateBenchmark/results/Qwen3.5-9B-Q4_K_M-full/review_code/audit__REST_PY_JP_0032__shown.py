import requests

def solve(inputs):
    url = "https://jsonplaceholder.typicode.com/users"
    payload = {"name": inputs["new_name"]}
    response = requests.post(url, json=payload)
    if response.status_code != 201:
        raise Exception(f"Failed to create user: {response.status_code} {response.text}")
    return None