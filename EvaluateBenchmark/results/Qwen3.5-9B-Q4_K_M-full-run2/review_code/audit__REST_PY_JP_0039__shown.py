def solve(inputs):
    """Retrieve a post by identifier from JSONPlaceholder and return its id or None."""
    import requests
    
    resource_id = inputs.get("resource_id")
    
    if resource_id is None:
        return None
    
    url = "https://jsonplaceholder.typicode.com/posts/{0}".format(resource_id)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if data is None:
            return None
        
        if "id" not in data:
            return None
        
        return data["id"]
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error: {e}")