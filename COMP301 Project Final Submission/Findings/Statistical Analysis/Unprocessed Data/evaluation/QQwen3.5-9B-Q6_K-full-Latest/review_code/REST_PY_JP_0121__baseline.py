import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_url = inputs['new_url']
    
    url = "https://jsonplaceholder.typicode.com/photos/1"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "id": resource_id,
        "url": new_url
    }

    response = requests.put(url, json=data, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update photo. Status code: {response.status_code}")
    
    if response.text.strip() == "":
        return None
    
    try:
        data = response.json()
        return data.get('title')
    except ValueError:
        return None