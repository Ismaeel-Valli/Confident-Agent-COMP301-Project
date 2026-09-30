import requests

def solve(inputs):
    """Retrieve a photo by identifier from JSONPlaceholder and return its title."""
    resource_id = inputs["resource_id"]
    
    url = "https://jsonplaceholder.typicode.com/photos"
    params = {"id": resource_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Return title if present, otherwise None
        return data.get("title")
    except requests.exceptions.HTTPError as e:
        raise e