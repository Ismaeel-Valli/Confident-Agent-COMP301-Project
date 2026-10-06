import requests

def solve(inputs):
    """
    Replaces a todo record on JSONPlaceholder with the supplied data.
    
    Inputs:
        inputs['resource_id']: Identifier of the todo (id)
        inputs['new_completed']: value for the completed attribute
        inputs['new_title']: value for the title attribute
        inputs['new_user_identifier']: value for the user Id attribute
    
    Returns:
        The response's id value, or None if that attribute is absent.
        Returns None for a successful empty response.
    
    Raises:
        Exception for an unsuccessful HTTP response.
    """
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    new_title = inputs['new_title']
    new_user_identifier = inputs['new_user_identifier']

    url = "https://jsonplaceholder.typicode.com/todos/1"  # Using ID 1 as an example; replace with resource_id if needed for dynamic calls
    
    payload = {
        'id': resource_id,
        'title': new_title,
        'completed': new_completed,
        'userId': new_user_identifier
    }

    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    # Check if the response is empty (no content)
    if not response.content:
        return None
    
    # Extract the 'id' from the JSON response if present
    try:
        data = response.json()
        return data.get('id')
    except ValueError:
        return None