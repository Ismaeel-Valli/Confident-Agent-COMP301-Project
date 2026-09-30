import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_completed = inputs["new_completed"]
    
    url = f"https://jsonplaceholder.typicode.com/todos/{resource_id}"
    payload = {"completed": new_completed}
    
    response = requests.patch(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    data = response.json()
    return data.get("id")