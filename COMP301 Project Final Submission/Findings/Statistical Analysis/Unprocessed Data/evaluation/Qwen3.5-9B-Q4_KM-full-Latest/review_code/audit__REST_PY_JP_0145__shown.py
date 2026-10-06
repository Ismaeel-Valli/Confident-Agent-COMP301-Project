import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_user_identifier = inputs["new_user_identifier"]
    
    url = f"https://jsonplaceholder.typicode.com/todos/{resource_id}"
    payload = {
        "userId": new_user_identifier
    }
    
    response = requests.patch(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data.get("id")
    else:
        return None