import requests

def solve(inputs):
    """
    Retrieve an album by identifier from JSONPlaceholder and return its id.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) for the album ID.
        
    Returns:
        int or None: The album's id, or None if absent or response is empty.
        
    Raises:
        requests.RequestException: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get("resource_id")
    if resource_id is None:
        return None
    
    url = "https://jsonplaceholder.typicode.com/albums"
    
    try:
        response = requests.get(url, params={"id": resource_id})
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            return None
            
        if "id" in data:
            return data["id"]
        else:
            return None
            
    except requests.RequestException as e:
        raise