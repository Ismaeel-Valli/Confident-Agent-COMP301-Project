import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    
    try:
        response = requests.delete(f"https://dummyjson.com/posts/{resource_id}")
        
        if response.status_code != 200:
            raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
        
        data = response.json()
        
        if 'isDeleted' in data and data['isDeleted']:
            return data['isDeleted']
        
        return None
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")