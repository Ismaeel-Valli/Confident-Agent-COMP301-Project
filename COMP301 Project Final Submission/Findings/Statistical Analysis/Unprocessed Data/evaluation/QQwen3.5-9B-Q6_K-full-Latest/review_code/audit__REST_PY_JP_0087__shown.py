import requests

def solve(inputs):
    """Retrieve a user by identifier from JSONPlaceholder and return their name."""
    resource_id = inputs.get("resource_id")
    
    if resource_id is None:
        return None
    
    url = "https://jsonplaceholder.typicode.com/users/{}".format(resource_id)
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for unsuccessful HTTP responses
        
        data = response.json()
        
        if data is None or not isinstance(data, dict):
            return None
            
        name = data.get("name")
        return name if name is not None else None
        
    except requests.exceptions.HTTPError:
        raise
    except Exception as e:
        raise