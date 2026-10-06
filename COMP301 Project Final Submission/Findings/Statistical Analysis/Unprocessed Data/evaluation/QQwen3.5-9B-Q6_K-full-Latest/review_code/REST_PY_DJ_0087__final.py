import requests

def solve(inputs):
    """
    Update selected fields of a user on DummyJSON.
    
    inputs:
        - resource_id: Identifier of the user (int)
        - new_age: value for the age attribute (int)
    
    Returns:
        - The response's id value if present, or None if absent.
        - None for a successful empty response.
        - Raises an exception for unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users"
    resource_id = inputs["resource_id"]
    new_age = inputs["new_age"]
    
    payload = {
        "id": resource_id,
        "age": new_age
    }
    
    response = requests.put(f"{base_url}/{resource_id}", json=payload)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update user: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Handle different possible response structures
    if "id" in data:
        return data["id"]
    elif "user" in data and isinstance(data["user"], dict) and "id" in data["user"]:
        return data["user"]["id"]
    else:
        return None