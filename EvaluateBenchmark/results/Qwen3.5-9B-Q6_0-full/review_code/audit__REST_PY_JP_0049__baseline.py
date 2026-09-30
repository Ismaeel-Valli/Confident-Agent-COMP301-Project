import requests

def solve(inputs):
    resource_id = inputs.get('resource_id')
    url = f"https://jsonplaceholder.typicode.com/albums/{resource_id}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data.get('id')