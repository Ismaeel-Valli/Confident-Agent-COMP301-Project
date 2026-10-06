import requests

def solve(inputs):
    """
    Submits a new user to JSONPlaceholder using the provided name.
    
    Args:
        inputs (dict): A dictionary containing 'new_name' for the user's name.
        
    Returns:
        dict or None: The decoded JSON response if successful, None otherwise.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    new_name = inputs.get('new_name')
    
    payload = {
        'name': new_name,
        'username': 'testuser',
        'email': 'test@example.com',
        'address': {
            'street': 'Test Street',
            'suite': '#0',
            'city': 'Test City',
            'zipcode': '12345',
            'geo': {
                'lat': '0.00',
                'lng': '0.00'
            }
        },
        'phone': '123-456-7890',
        'website': 'example.com',
        'company': {
            'name': 'Test Company',
            'catchPhrase': 'Test Catch Phrase',
            'bs': 'test'
        }
    }

    response = requests.post(url, json=payload)
    
    if response.status_code == 201:
        return None
    elif response.status_code == 200:
        return response.json()
    else:
        raise requests.RequestException(f"Failed to create user. Status code: {response.status_code}")