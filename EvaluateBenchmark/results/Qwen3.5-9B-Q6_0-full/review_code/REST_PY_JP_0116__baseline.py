import requests

def solve(inputs):
    """
    Submits a new comment to JSONPlaceholder with updated name and email,
    then returns the name from the response or None if absent/successful empty response.
    
    Args:
        inputs (dict): Contains 'new_email' and 'new_name'.
        
    Returns:
        str or None: The name from the response, or None if successful with no name.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    
    # Prepare the payload for updating a comment (ID 1 is assumed to exist)
    payload = {
        "id": 1,
        "name": inputs["new_name"],
        "email": inputs["new_email"]
    }
    
    try:
        response = requests.put(f"{base_url}/comments/1", json=payload)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        if response.status_code == 200:
            data = response.json()
            return data.get("name")
        elif response.status_code == 204:
            return None
        else:
            raise requests.HTTPError(f"Unexpected status code: {response.status_code}")
            
    except requests.RequestException as e:
        raise e