import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_completed = inputs["new_completed"]
    new_user_identifier = inputs["new_user_identifier"]
    
    base_url = "https://dummyjson.com"
    url = f"{base_url}/todos/{resource_id}"
    
    payload = {
        "completed": new_completed,
        "userId": new_user_identifier
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("id")
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to update todo: {response.status_code} {response.text}")