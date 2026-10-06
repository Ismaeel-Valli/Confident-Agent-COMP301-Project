import requests

def solve(inputs):
    resource_id = inputs.get('resource_id')
    
    url = f"https://jsonplaceholder.typicode.com/users/{resource_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    name = data.get('name')
    
    if name is None:
        return None
        
    return name