import requests

def solve(inputs):
    """
    Updates a Todo item on JSONPlaceholder with new 'completed' status.
    
    Args:
        inputs (dict): Contains 'resource_id' (int) and 'new_completed' (bool).
        
    Returns:
        int or None: The updated todo's id if present in response, otherwise None for success.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not 200 or 204).
    """
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    
    url = "https://jsonplaceholder.typicode.com/todos/1"
    payload = {
        "id": resource_id,
        "userId": 1,
        "title": "delectus aut autem",
        "completed": new_completed
    }
    
    response = requests.patch(url, json=payload)
    
    if response.status_code not in [200, 204]:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    if response.status_code == 204:
        return None
    
    data = response.json()
    return data.get('id')