import requests

def solve(inputs):
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/users"
    
    payload = {"name": inputs["new_name"]}
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 201:
        data = response.json()
        return data.get("name")
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to create user. Status code: {response.status_code}")