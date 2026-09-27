import requests

def solve(inputs):
    user_identifier = inputs["user_identifier"]
    url = f"https://jsonplaceholder.typicode.com/users/{user_identifier}/albums"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}")
    return response.json()