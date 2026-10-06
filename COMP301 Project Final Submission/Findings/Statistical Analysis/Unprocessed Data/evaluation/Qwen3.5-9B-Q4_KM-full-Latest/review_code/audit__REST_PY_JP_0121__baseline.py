import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_url = inputs['new_url']
    
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {"url": new_url}
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code}")
    
    data = response.json()
    
    if 'title' in data and data['title'] is not None:
        return data['title']
    elif response.status_code == 204 or (not data and response.status_code == 200):
        return None
    
    return None