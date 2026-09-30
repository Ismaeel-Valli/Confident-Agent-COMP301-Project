import requests

def solve(inputs):
    """Retrieve a photo by identifier from JSONPlaceholder and return its id."""
    resource_id = inputs.get("resource_id")
    
    if resource_id is None:
        return None
    
    url = "https://jsonplaceholder.typicode.com/photos"
    params = {"id": resource_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for unsuccessful HTTP responses
        
        data = response.json()
        
        if isinstance(data, dict):
            return data.get("id")
        elif isinstance(data, list):
            if len(data) == 0:
                return None
            return data[0].get("id")
        else:
            return None
            
    except requests.exceptions.HTTPError:
        raise
    except requests.exceptions.RequestException:
        raise