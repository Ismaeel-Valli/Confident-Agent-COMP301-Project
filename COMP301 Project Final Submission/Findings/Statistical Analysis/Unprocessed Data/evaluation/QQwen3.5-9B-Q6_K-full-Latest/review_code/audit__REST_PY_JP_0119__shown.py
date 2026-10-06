import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_user_identifier = inputs["new_user_identifier"]
    
    url = f"https://jsonplaceholder.typicode.com/albums/{resource_id}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "userId": new_user_identifier
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data.get("title")
    else:
        raise Exception(f"Failed to update album: {response.status_code} - {response.text}")