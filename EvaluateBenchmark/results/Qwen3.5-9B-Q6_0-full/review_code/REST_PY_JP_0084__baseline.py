import requests

def solve(inputs):
    """
    Replaces a todo record in JSONPlaceholder with supplied data.
    
    Parameters:
        inputs (dict): Contains 'resource_id', 'new_completed', 'new_title', 'new_user_identifier'.
        
    Returns:
        str or None: The title from the response if present, otherwise None for success.
        Raises: Exception on unsuccessful HTTP response.
    """
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    new_title = inputs['new_title']
    new_user_identifier = inputs['new_user_identifier']

    url = "https://jsonplaceholder.typicode.com/todos/1"  # Note: JSONPlaceholder uses fixed IDs for PUT, typically 1
    
    payload = {
        'id': resource_id,
        'title': new_title,
        'completed': new_completed,
        'userId': new_user_identifier
    }

    response = requests.put(url, json=payload)

    if response.status_code != 200:
        raise Exception(f"Failed to update todo. Status code: {response.status_code}")

    # JSONPlaceholder returns an empty body on successful PUT for this endpoint in some versions/configs
    # or the updated object. We follow the instruction: return title if present, else None.
    data = response.json()
    
    if isinstance(data, dict) and 'title' in data:
        return data['title']
    
    return None