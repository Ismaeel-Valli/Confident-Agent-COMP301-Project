import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_user_identifier = inputs["new_user_identifier"]
    
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/albums/{resource_id}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "userId": new_user_identifier
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if "title" in data and data["title"] is not None:
        return data["title"]
    else:
        return None