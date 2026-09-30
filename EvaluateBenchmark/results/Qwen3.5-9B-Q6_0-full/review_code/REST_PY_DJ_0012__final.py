import requests

def solve(inputs):
    """
    Submit a new user to DummyJSON using the provided first name.
    
    Args:
        inputs (dict): Must contain 'new_firstName' key with the first name value.
        
    Returns:
        dict or None: The decoded JSON response, or None if successful and empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/users/add"
    
    payload = {
        "firstName": inputs["new_firstName"],
        "lastName": "Doe",
        "email": f"{inputs['new_firstName'].lower()}@example.com",
        "age": 30,
        "gender": "male",
        "phone": "+1234567890",
        "dateOfBirth": "1990-01-01",
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zipCode": "10001",
            "country": "USA"
        },
        "picture": {
            "large": "https://dummyjson.com/image/placeholder",
            "thumbnail": "https://dummyjson.com/image/placeholder"
        }
    }
    
    response = requests.post(base_url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
    
    return response.json()