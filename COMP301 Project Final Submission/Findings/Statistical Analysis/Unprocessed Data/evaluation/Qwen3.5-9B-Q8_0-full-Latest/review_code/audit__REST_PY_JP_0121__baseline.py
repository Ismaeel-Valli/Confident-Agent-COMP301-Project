import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_url = inputs['new_url']
    
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "url": new_url
    }
    
    response = requests.patch(url, json=data, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")
    
    if response.text.strip() == "":
        return None
    
    try:
        json_response = response.json()
        return json_response.get('title')
    except ValueError:
        return None