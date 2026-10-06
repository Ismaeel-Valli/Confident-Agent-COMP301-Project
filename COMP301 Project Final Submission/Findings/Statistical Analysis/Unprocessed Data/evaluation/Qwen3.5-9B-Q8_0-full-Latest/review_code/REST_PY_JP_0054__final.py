import requests

def solve(inputs):
    """Retrieve a photo by identifier from JSONPlaceholder and return its id."""
    resource_id = inputs["resource_id"]
    
    url = "https://jsonplaceholder.typicode.com/photos"
    params = {"id": resource_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Return the id if present, otherwise None
        return data.get("id")
    except requests.exceptions.HTTPError:
        raise