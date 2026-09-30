import requests

def solve(inputs):
    """
    Replaces a user record in JSONPlaceholder with supplied data.
    
    Args:
        inputs (dict): Contains 'resource_id', 'new_email', 'new_name', 
                       'new_phone', 'new_username', 'new_website'.
    
    Returns:
        str or None: The name value from the response, or None if absent or successful empty response.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    new_email = inputs['new_email']
    new_name = inputs['new_name']
    new_phone = inputs['new_phone']
    new_username = inputs['new_username']
    new_website = inputs['new_website']

    url = "https://jsonplaceholder.typicode.com/users"
    
    payload = {
        'id': resource_id,
        'name': new_name,
        'username': new_username,
        'email': new_email,
        'phone': new_phone,
        'website': new_website
    }

    response = requests.put(url, json=payload)
    
    if not response.ok:
        raise requests.exceptions.HTTPError(f"Request failed with status code: {response.status_code}")
    
    return response.json().get('name')