import requests

def solve(inputs):
    """
    Replaces a todo record in JSONPlaceholder with supplied data.
    
    Parameters:
        inputs (dict): Contains 'resource_id', 'new_completed', 'new_title', 'new_user_identifier'.
        
    Returns:
        str or None: The title from the response, or None if successful but empty response.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    new_title = inputs['new_title']
    new_user_identifier = inputs['new_user_identifier']

    url = "https://jsonplaceholder.typicode.com/todos/1"  # Note: JSONPlaceholder uses fixed IDs, but we'll use the provided resource_id in the URL.
    # However, JSONPlaceholder does not support PUT/PATCH with custom IDs other than 1 for todos.
    # To adhere to the problem statement which implies using the given resource_id, we construct the URL accordingly.
    url = f"https://jsonplaceholder.typicode.com/todos/{resource_id}"

    payload = {
        "completed": new_completed,
        "title": new_title,
        "userId": new_user_identifier
    }

    try:
        response = requests.put(url, json=payload)
        response.raise_for_status()
        
        if response.status_code == 204:
            return None
        
        data = response.json()
        return data.get('title')
    
    except requests.RequestException as e:
        raise e