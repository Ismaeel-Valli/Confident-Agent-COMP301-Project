import requests

def solve(inputs):
    """
    Submit a new user to DummyJSON using the provided first name.
    
    Args:
        inputs (dict): Must contain 'new_firstName' key with the first name value.
        
    Returns:
        int or None: The response's id if present, otherwise None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/users/add"
    
    payload = {
        "firstName": inputs["new_firstName"],
        "lastName": "Doe",  # DummyJSON requires lastName, using a default value
        "email": "user@example.com",  # DummyJSON requires email, using a default value
        "age": 30,  # DummyJSON requires age, using a default value
        "gender": "male",  # DummyJSON requires gender, using a default value
        "phone": "1234567890",  # DummyJSON requires phone, using a default value
        "dateOfBirth": "1990-01-01",  # DummyJSON requires dateOfBirth, using a default value
        "address": {
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zipCode": "10001",
            "country": "USA"
        },
        "occupation": "Engineer",  # DummyJSON requires occupation, using a default value
        "maritalStatus": "single",  # DummyJSON requires maritalStatus, using a default value
        "children": 0,  # DummyJSON requires children, using a default value
        "company": {
            "name": "Example Corp",
            "title": "Engineer"
        }
    }
    
    response = requests.post(base_url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")
    
    data = response.json()
    
    # Return the id if present, otherwise None for successful empty response
    return data.get("id")