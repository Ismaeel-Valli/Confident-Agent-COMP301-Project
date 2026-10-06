import requests

def solve(inputs):
    """
    Update a todo item in DummyJSON and return its id or None.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) and 'new_todo' (str).
        
    Returns:
        int or None: The updated todo's id, or None if absent or response is empty.
        
    Raises:
        Exception: If the HTTP response indicates failure (status >= 400).
    """
    resource_id = inputs['resource_id']
    new_todo = inputs['new_todo']
    
    base_url = "https://dummyjson.com"
    url = f"{base_url}/todos/{resource_id}"
    
    payload = {
        "todo": new_todo
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update todo: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # DummyJSON PUT /todos/{id} returns the updated todo object directly
    if 'id' in data:
        return data['id']
    elif response.status_code == 204:
        return None
    else:
        return None