import requests

def solve(inputs):
    """
    Submits a new user to JSONPlaceholder using the provided inputs dictionary.
    
    Args:
        inputs (dict): A dictionary containing 'new_name' for the user's name.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    # Prepare the payload with the provided name and other required fields
    payload = {
        "name": inputs["new_name"],
        "username": "auto-generated-username",  # JSONPlaceholder requires this
        "email": "auto-generated-email@example.com",  # JSONPlaceholder requires this
        "address": {
            "street": "1234 Fake Street",
            "suite": "Apt. 101",
            "city": "New York",
            "zipcode": "10001",
            "geo": {
                "lat": "37.5929",
                "lng": "-122.0843"
            }
        },
        "phone": "1-202-555-0100",
        "website": "example.com",
        "company": {
            "name": "Example Corp",
            "catchPhrase": "Example Catch Phrase",
            "bs": "example business"
        }
    }
    
    response = requests.post(url, json=payload)
    
    # Raise an exception for unsuccessful HTTP responses (status code outside 200-299)
    response.raise_for_status()
    
    # Return None for a successful empty response (e.g., 201 Created with no content)
    if response.status_code == 201 and not response.content:
        return None
    
    # Decode and return the JSON response
    try:
        return response.json()
    except ValueError:
        raise requests.exceptions.RequestException("Failed to decode JSON response")