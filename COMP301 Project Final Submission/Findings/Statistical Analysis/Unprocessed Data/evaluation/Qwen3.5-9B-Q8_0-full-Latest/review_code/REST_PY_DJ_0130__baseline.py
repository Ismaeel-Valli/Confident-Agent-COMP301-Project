import requests

def solve(inputs):
    """
    Updates selected fields of a todo in DummyJSON API.
    
    Args:
        inputs (dict): Contains 'resource_id', 'new_todo', and 'new_user_identifier'
    
    Returns:
        str or None: The response's id value, or None if absent or successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    resource_id = inputs['resource_id']
    new_todo = inputs['new_todo']
    new_user_identifier = inputs['new_user_identifier']
    
    # Construct the update payload
    payload = {
        "todo": new_todo,
        "user_id": new_user_identifier
    }
    
    # Make PATCH request to DummyJSON API
    url = f"https://dummyjson.com/todos/{resource_id}"
    response = requests.patch(url, json=payload)
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Check if response is empty (successful but no content)
    if not response.text:
        return None
    
    # Parse JSON response
    try:
        data = response.json()
        # Return the id from the response if present
        return data.get('id')
    except ValueError:
        # If response is not valid JSON, return None
        return None