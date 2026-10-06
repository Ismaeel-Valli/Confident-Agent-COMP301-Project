import requests

def solve(inputs):
    """
    Update a user's name in JSONPlaceholder and return the updated name.
    
    Args:
        inputs (dict): Dictionary containing:
            - resource_id (int): The ID of the user to update.
            - new_name (str): The new name value.
    
    Returns:
        str or None: The updated name from the response, or None if absent.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs["resource_id"]
    new_name = inputs["new_name"]
    
    url = f"{base_url}/users/{resource_id}"
    payload = {"name": new_name}
    
    response = requests.put(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data.get("name")
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to update user: {response.status_code} - {response.text}")