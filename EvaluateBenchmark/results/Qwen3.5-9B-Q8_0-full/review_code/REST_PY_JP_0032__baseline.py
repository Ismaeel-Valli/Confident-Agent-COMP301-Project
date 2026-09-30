import requests

def solve(inputs):
    """
    Submits a new user to JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing 'new_name' for the user's name.
        
    Returns:
        dict or None: The decoded JSON response if successful, None for empty response.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    # Prepare the payload with the provided name and other required fields
    payload = {
        "name": inputs["new_name"],
        "username": "auto-generated-username",  # Placeholder as JSONPlaceholder requires it
        "email": f"{inputs['new_name'].lower()}@example.com",  # Placeholder email
        "address": {
            "street": "123 Main St",
            "suite": "Apt 0",
            "city": "New York",
            "zipcode": "10001",
            "geo": {
                "lat": "40.7128",
                "lng": "-74.0060"
            }
        },
        "phone": "555-555-5555",
        "website": "example.com"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        if response.status_code == 201 and len(response.content) == 0:
            return None
            
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to submit user: {str(e)}") from e