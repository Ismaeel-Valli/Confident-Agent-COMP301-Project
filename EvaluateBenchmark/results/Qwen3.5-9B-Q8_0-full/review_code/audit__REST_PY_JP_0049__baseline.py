import requests

def solve(inputs):
    resource_id = inputs.get('resource_id')
    
    if resource_id is None:
        return None
    
    url = f"https://jsonplaceholder.typicode.com/albums/{resource_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        if response.status_code == 200:
            data = response.json()
            if not data:
                return None
            return data.get('id')
        else:
            raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")