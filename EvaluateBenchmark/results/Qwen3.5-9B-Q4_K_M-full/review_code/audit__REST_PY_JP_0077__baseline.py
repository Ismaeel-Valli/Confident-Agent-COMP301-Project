import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    
    url = f"https://jsonplaceholder.typicode.com/albums/{resource_id}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {"title": new_title}
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    title = data.get("title")
    
    if not title:
        return None
    
    return title