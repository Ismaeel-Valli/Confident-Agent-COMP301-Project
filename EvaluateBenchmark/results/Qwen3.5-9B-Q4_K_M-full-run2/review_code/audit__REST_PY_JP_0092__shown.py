import requests

def solve(inputs):
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/comments"
    
    payload = {
        "email": inputs["new_email"],
        "name": inputs["new_name"]
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    data = response.json()
    
    if isinstance(data, list):
        return None
    
    return data