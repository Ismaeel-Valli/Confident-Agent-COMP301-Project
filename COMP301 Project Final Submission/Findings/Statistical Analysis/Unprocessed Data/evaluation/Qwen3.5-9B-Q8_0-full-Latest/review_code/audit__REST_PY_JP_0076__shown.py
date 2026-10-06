import requests

def solve(inputs):
    """
    Replace an album record in JSONPlaceholder with supplied data.
    
    Inputs:
        inputs['resource_id']: int - ID of the album to replace
        inputs['new_title']: str - New title value
        inputs['new_user_identifier']: int - New user ID value
    
    Returns:
        str - The response's title value, or None if absent or successful empty response
        None for a successful empty response (as per instructions)
    
    Raises:
        Exception - For unsuccessful HTTP responses
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    new_user_identifier = inputs['new_user_identifier']
    
    url = f"{base_url}/albums/{resource_id}"
    
    payload = {
        'title': new_title,
        'userId': new_user_identifier
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return title if present, otherwise None
    if 'title' in data and data['title'] is not None:
        return data['title']
    else:
        return None