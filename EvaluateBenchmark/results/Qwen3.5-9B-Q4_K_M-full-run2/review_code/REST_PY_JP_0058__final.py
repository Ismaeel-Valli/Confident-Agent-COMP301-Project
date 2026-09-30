import requests

def solve(inputs):
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/todos"
    
    payload = {
        "title": inputs["new_title"],
        "userId": 1,
        "body": "Body"
    }
    
    response = requests.post(url, json=payload)
    if response.status_code != 201:
        raise Exception(f"Failed to create todo: {response.status_code}")
    
    data = response.json()
    return data.get("id")