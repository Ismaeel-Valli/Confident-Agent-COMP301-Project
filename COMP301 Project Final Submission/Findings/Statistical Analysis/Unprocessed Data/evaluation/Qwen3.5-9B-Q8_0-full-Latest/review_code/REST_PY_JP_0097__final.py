import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_url = inputs['new_url']
    
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    
    payload = {
        "id": resource_id,
        "userId": 1,
        "albumId": 1,
        "title": "foo",
        "userStatus": 0,
        "url": new_url,
        "thumbnailUrl": "http://dummyjson.com/image/400x200.jpg"
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code >= 400:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    return response.json() if response.content else None