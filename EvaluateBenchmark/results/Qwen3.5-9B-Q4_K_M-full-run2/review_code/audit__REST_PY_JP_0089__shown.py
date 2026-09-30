import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_name = inputs["new_name"]
    
    url = f"https://jsonplaceholder.typicode.com/users/{resource_id}"
    payload = {"name": new_name}
    
    response = requests.put(url, json=payload)
    response.raise_for_status()
    
    if response.status_code == 200:
        return response.json().get("name")
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")