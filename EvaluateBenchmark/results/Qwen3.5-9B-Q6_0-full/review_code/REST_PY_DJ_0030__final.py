import requests

def solve(inputs):
    """Retrieve a user by identifier from DummyJSON and return the user's id."""
    try:
        response = requests.get(
            "https://dummyjson.com/users",
            params={"id": inputs["resource_id"]}
        )
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            # DummyJSON returns a list of users, so we need to find the user with matching id
            for user in data.get("users", []):
                if user.get("id") == inputs["resource_id"]:
                    return user.get("id")
            return None  # User not found
        
        raise Exception(f"Unexpected status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")