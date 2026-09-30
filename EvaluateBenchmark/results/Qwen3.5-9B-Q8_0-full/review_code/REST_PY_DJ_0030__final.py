import requests

def solve(inputs):
    """Retrieve a user by identifier from DummyJSON and return the user's id."""
    resource_id = inputs.get("resource_id")
    
    if resource_id is None:
        return None
    
    try:
        response = requests.get(
            "https://dummyjson.com/users",
            params={"id": resource_id}
        )
        
        if response.status_code != 200:
            raise Exception(f"HTTP error: {response.status_code}")
        
        data = response.json()
        
        # Check if the response contains a 'user' key with user data
        if "user" in data and data["user"]:
            return data["user"].get("id")
        else:
            return None
            
    except requests.RequestException as e:
        raise Exception(f"Request failed: {e}")