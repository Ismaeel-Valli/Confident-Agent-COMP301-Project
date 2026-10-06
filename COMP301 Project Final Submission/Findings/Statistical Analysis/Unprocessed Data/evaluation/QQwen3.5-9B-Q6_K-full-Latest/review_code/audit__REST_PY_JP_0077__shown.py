import requests

def solve(inputs):
    resource_id = inputs["resource_id"]
    new_title = inputs["new_title"]
    
    url = f"https://jsonplaceholder.typicode.com/albums/{resource_id}"
    payload = {
        "title": new_title
    }
    
    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update album: {response.status_code}")
    
    data = response.json()
    return data.get("title")