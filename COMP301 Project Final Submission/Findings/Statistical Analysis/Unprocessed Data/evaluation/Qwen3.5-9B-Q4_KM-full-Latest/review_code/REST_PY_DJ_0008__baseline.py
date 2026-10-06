import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    url = f"https://dummyjson.com/users/{resource_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code}")
    
    data = response.json()
    
    if not data['users']:
        return None
    
    return data['users'][0]