import requests

def solve(inputs):
    """
    Updates selected fields of a user in DummyJSON API and returns the response's id value.
    
    Args:
        inputs (dict): Dictionary containing:
            - resource_id (str): Identifier of the user
            - new_lastName (str): New value for the last name attribute
    
    Returns:
        str or None: The ID from the response if present, otherwise None for successful empty responses.
    
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    new_last_name = inputs['new_lastName']
    
    # Base URL for DummyJSON API
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/users/{resource_id}"
    
    # Prepare the payload with only the field to update
    payload = {
        "lastName": new_last_name
    }
    
    try:
        response = requests.put(url, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        # Check if the response is empty
        if not response.text.strip():
            return None
        
        # Try to extract the id from the response
        try:
            data = response.json()
            return data.get('id')
        except ValueError:
            # If JSON parsing fails, return None as per requirements for non-empty but invalid responses
            return None
            
    except requests.RequestException as e:
        raise e