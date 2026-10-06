import requests

def solve(inputs):
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs["resource_id"]
    new_name = inputs["new_name"]
    
    url = f"{base_url}/users/{resource_id}"
    headers = {"Content-Type": "application/json"}
    payload = {"name": new_name}
    
    response = requests.put(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    return data.get("name")