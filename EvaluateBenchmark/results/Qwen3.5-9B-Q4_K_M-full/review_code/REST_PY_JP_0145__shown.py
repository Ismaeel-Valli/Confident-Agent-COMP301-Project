def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_user_identifier = inputs["new_user_identifier"]
    
    url = "https://jsonplaceholder.typicode.com/todos/1"
    payload = {
        "userId": new_user_identifier,
        "id": resource_id,
        "title": "foo",
        "completed": True
    }
    
    response = requests.patch(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 200:
        return None
    
    if response.status_code == 204:
        return None
    
    return response.json().get("id")