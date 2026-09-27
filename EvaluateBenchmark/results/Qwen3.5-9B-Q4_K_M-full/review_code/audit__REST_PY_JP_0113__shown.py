def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_username = inputs["new_username"]
    
    url = f"https://jsonplaceholder.typicode.com/users/{resource_id}"
    payload = {"username": new_username}
    
    response = requests.patch(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    data = response.json()
    return data.get("id")