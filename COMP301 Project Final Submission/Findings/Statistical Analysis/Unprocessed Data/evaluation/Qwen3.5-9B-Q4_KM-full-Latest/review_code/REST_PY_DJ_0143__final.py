import requests

def solve(inputs):
    base_url = "https://dummyjson.com/users"
    params = {"sort": inputs["sort_field"], "sortDir": inputs["sort_direction"]}
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    data = response.json()
    return data.get("users")