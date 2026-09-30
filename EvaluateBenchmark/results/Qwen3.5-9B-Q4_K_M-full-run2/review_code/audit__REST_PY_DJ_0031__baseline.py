import requests

def solve(inputs):
    """
    Updates selected fields of a user via DummyJSON API and returns the response ID or None.
    
    Args:
        inputs (dict): Contains 'resource_id' (user ID) and 'new_firstName'.
        
    Returns:
        str or None: The 'id' from the response if present, otherwise None for empty success response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs.get('resource_id')
    new_first_name = inputs.get('new_firstName')
    
    url = f"https://httpbin.org/put"
    data = {
        "id": resource_id,
        "firstName": new_first_name
    }
    
    response = requests.put(url, json=data)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    # DummyJSON typically returns the updated object or an empty response on success
    response_json = response.json()
    
    if 'id' in response_json:
        return response_json['id']
    else:
        return None