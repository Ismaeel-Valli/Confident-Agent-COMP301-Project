import requests

def solve(inputs):
    resource_id = inputs.get("resource_id")
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve users: {response.status_code}")
    
    users = response.json()
    for user in users:
        if user["id"] == resource_id:
            return user.get("id")
    
    return None