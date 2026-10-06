import requests

def solve(inputs):
    """
    Submits a new user to JSONPlaceholder using the provided name.
    
    Args:
        inputs (dict): A dictionary containing 'new_name' for the user's name attribute.
        
    Returns:
        str or None: The response's 'name' value if present, otherwise None for a successful empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    new_name = inputs.get('new_name')
    
    payload = {
        'name': new_name,
        'username': 'testuser',
        'email': 'test@example.com',
        'address': {'street': 'test street', 'suite': 'A.0.0', 'city': 'Test City', 'zipcode': '12345', 'geo': {'lat': '22', 'lng': '-3'}},
        'phone': '123-456-7890',
        'website': 'test.com'
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
        
    data = response.json()
    
    if 'name' in data:
        return data['name']
    else:
        return None