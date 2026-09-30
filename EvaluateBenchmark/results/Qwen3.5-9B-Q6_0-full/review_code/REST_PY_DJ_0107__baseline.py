import requests

def solve(inputs):
    """
    Updates selected fields of a user in DummyJSON API.
    
    Args:
        inputs (dict): Contains 'resource_id' (user ID) and 'new_email' (new email value).
        
    Returns:
        str or None: The response's id value if present, otherwise None for successful empty responses.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    new_email = inputs.get('new_email')
    
    # DummyJSON API endpoint for updating a user
    url = f"https://dummyjson.com/users/update/{resource_id}"
    
    payload = {
        "email": new_email
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Check if the response is empty (successful update with no data returned)
    if not response.text:
        return None
    
    # Parse the JSON response
    try:
        response_data = response.json()
        
        # Return the id value if present, otherwise None
        return response_data.get('id')
    except ValueError:
        # If response is not valid JSON but we got a successful status code
        return None