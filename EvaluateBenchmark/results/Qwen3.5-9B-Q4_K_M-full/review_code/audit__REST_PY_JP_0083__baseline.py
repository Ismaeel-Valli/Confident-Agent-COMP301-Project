import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    
    url = f"https://jsonplaceholder.typicode.com/todos/{resource_id}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data.get('title')