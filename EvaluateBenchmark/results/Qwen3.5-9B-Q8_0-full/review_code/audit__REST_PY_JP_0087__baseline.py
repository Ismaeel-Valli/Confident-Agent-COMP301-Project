import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/users/{resource_id}")
        
        if response.status_code != 200:
            raise Exception(f"HTTP error occurred: {response.status_code}")
        
        data = response.json()
        
        if not data:
            return None
        
        return data.get('name')
    
    except requests.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")