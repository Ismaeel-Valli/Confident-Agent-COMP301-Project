import requests

def solve(inputs):
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/todos"
    
    payload = {
        "title": inputs["new_title"],
        "body": "",
        "userId": 1
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create todo. Status code: {response.status_code}")
    
    return response.json()