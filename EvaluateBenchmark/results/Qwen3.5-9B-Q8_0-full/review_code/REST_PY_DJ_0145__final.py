import requests

def solve(inputs):
    """
    Submit a new user to DummyJSON and return the response's id value,
    or None if that attribute is absent. Return None for a successful empty response.
    Raise an exception for an unsuccessful HTTP response.
    
    Args:
        inputs (dict): Dictionary containing 'new_firstName' and 'new_username'.
        
    Returns:
        int or None: The id of the created user, or None if absent or on empty response.
        
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/users/add"
    
    payload = {
        "firstName": inputs["new_firstName"],
        "username": inputs["new_username"]
    }
    
    try:
        response = requests.post(base_url, json=payload)
        
        if response.status_code >= 400:
            raise requests.RequestException(f"HTTP {response.status_code}: {response.text}")
        
        # Check if the response is empty (no content or no id in data)
        if not response.content:
            return None
            
        data = response.json()
        
        # DummyJSON returns a dict with 'data' field containing the user list on POST /users/add
        if isinstance(data, dict):
            users_list = data.get("data", [])
            if isinstance(users_list, list) and len(users_list) > 0:
                user_id = users_list[0].get("id")
                return user_id if user_id is not None else None
            
            # If 'data' is not a list but has an 'id' field directly
            user_id = data.get("id")
            return user_id if user_id is not None else None
        
        return None
        
    except requests.RequestException as e:
        raise