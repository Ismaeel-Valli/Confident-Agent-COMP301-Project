import requests

def solve(inputs):
    """
    Update a user in JSONPlaceholder with new name.
    
    Args:
        inputs (dict): Must contain 'resource_id' and 'new_name'.
        
    Returns:
        str or None: The updated name from the response, or None if absent.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    new_name = inputs['new_name']
    
    url = "https://jsonplaceholder.typicode.com/users/{}".format(resource_id)
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    payload = {
        'name': new_name
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception("Failed to update user. Status code: {}".format(response.status_code))
    
    data = response.json()
    
    name = data.get('name')
    
    return name