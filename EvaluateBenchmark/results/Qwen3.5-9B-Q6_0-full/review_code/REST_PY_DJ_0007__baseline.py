import requests

def solve(inputs):
    """
    Retrieves one page of users from DummyJSON API.
    
    Args:
        inputs (dict): A dictionary containing 'page' key (int) specifying the page number.
        
    Returns:
        list or None: The decoded JSON response as a list of users, or None if the response is empty.
        
    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code indicates an error.
    """
    base_url = "https://dummyjson.com/users"
    
    # Extract page number from inputs, default to 1 if not provided or invalid
    try:
        page = int(inputs.get('page', 1))
    except (ValueError, TypeError):
        raise ValueError("Page number must be an integer")

    params = {
        'page': page,
        'limit': 10  # Standard limit for one page
    }

    response = requests.get(base_url, params=params)
    
    if not response.ok:
        raise requests.exceptions.HTTPError(f"HTTP error occurred: {response.status_code}")
    
    data = response.json()
    
    # Return None if the users array is empty
    if not data.get('users'):
        return None
        
    return data['users']