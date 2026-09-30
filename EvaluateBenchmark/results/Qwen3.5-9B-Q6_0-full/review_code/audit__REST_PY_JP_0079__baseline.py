import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        if response.status_code == 200 and not response.json():
            return None
        
        data = response.json()
        return data.get('title')
    
    except requests.exceptions.HTTPError:
        raise