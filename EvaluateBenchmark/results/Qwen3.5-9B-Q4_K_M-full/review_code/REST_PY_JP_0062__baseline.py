import requests

def solve(inputs):
    """
    Submits a new user to JSONPlaceholder using the provided name.
    
    Args:
        inputs (dict): A dictionary containing 'new_name' for the user's name attribute.
        
    Returns:
        int or None: The response's id value if present, or None if the response is empty/successful without an ID.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    url = "https://jsonplaceholder.typicode.com/users"
    new_name = inputs.get('new_name')
    
    payload = {
        'name': new_name,
        'username': 'testuser',
        'email': 'test@example.com',
        'address': {'street': 'test street', 'suite': 'Apt. 5', 'city': 'New York', 'zipcode': '10001', 'geo': {'lat': '42.38', 'lng': '-71.11'}},
        'phone': '555-555-5555',
        'website': 'example.com'
    }

    response = requests.post(url, json=payload)

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")

    data = response.json()
    
    # JSONPlaceholder typically returns the created object with an 'id' field.
    # However, per instructions: return None for a successful empty response.
    if not data:
        return None
    
    return data.get('id')