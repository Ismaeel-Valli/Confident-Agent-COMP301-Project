def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_todo = inputs["new_todo"]
    new_user_identifier = inputs["new_user_identifier"]
    
    base_url = "https://dummyjson.com"
    url = f"{base_url}/todos/{resource_id}"
    
    headers = {
        "Content-Type": "application/json",
    }
    
    payload = {
        "todo": new_todo,
        "userId": new_user_identifier,
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    if "id" in data:
        return data["id"]
    else:
        return None