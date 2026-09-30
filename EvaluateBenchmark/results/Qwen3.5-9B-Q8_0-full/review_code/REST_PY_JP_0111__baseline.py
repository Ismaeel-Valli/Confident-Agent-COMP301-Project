import requests

def solve(inputs):
    """
    Updates a todo item in JSONPlaceholder with new completion status.
    
    Args:
        inputs (dict): Contains 'resource_id' (int) and 'new_completed' (bool).
        
    Returns:
        int or None: The ID of the updated todo, or None if response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    
    url = "https://jsonplaceholder.typicode.com/todos/1"
    
    payload = {
        'id': resource_id,
        'completed': new_completed
    }
    
    try:
        response = requests.patch(url, json=payload)
        response.raise_for_status()
        
        if response.status_code == 204:
            return None
            
        data = response.json()
        return data.get('id')
        
    except requests.RequestException as e:
        raise e