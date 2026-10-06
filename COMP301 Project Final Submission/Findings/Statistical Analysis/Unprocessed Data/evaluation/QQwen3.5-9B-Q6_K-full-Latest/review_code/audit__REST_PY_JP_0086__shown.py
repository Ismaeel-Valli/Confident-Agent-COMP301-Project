import requests


def solve(inputs):
    """Submit a new user to JSONPlaceholder and return the name or None."""
    url = "https://jsonplaceholder.typicode.com/users"
    payload = {"name": inputs["new_name"]}

    response = requests.post(url, json=payload)
    response.raise_for_status()

    if response.status_code == 201:
        data = response.json()
        return data.get("name")
    elif response.status_code == 200:
        # Successful empty response
        return None
    else:
        raise Exception(f"Failed to create user: {response.status_code} - {response.text}")