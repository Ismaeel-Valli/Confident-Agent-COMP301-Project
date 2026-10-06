import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    url = f"https://dummyjson.com/products/{resource_id}"
    
    try:
        response = requests.delete(url)
        response.raise_for_status()
        
        if response.status_code == 204:
            return None
        
        data = response.json()
        return data.get('isDeleted')
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")