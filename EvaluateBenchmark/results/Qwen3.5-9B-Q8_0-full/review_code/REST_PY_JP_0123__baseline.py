import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    
    url = "https://jsonplaceholder.typicode.com/todos/1"
    payload = {
        "id": resource_id,
        "completed": new_completed
    }
    
    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update todo. Status code: {response.status_code}")
    
    data = response.json()
    
    if data is None or 'title' not in data:
        return None
    
    return data['title']