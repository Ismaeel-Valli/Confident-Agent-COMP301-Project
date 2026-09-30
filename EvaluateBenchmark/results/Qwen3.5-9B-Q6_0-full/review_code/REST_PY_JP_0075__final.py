import requests

def solve(inputs):
    """Retrieve an album by identifier from JSONPlaceholder and return its title."""
    resource_id = inputs.get("resource_id")
    
    if resource_id is None:
        return None
    
    url = "https://jsonplaceholder.typicode.com/albums"
    params = {"id": resource_id}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if isinstance(data, dict):
            title = data.get("title")
            return title if title is not None else None
        elif isinstance(data, list):
            if len(data) == 0:
                return None
            # If it's a list and the first item has a title, return it
            if len(data) > 0 and "title" in data[0]:
                return data[0]["title"]
            return None
        else:
            return None
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except ValueError as e:
        raise Exception(f"Invalid JSON response: {e}")