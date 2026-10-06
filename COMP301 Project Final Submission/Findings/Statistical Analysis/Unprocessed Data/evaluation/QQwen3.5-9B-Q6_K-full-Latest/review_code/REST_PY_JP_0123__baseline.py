import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_completed = inputs['new_completed']
    
    url = "https://jsonplaceholder.typicode.com/todos/1"
    payload = {
        "id": resource_id,
        "userId": 1,
        "title": "foo",
        "completed": new_completed
    }

    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data.get('title')