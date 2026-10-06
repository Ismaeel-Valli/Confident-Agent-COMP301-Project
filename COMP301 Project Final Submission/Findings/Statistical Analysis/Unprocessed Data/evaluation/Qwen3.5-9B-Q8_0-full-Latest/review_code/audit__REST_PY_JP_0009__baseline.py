import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    url = f"https://jsonplaceholder.typicode.com/comments/{resource_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        if response.status_code == 200 and not response.json():
            return None
        
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")