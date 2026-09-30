import requests

def solve(inputs):
    """Delete a post by identifier from DummyJSON and return the response's id or None."""
    resource_id = inputs.get("resource_id")
    if resource_id is None:
        return None
    
    url = "https://dummyjson.com/posts/{id}".format(id=resource_id)
    try:
        response = requests.delete(url)
        response.raise_for_status()
        
        data = response.json()
        if data.get("success") is True:
            return None
        
        return data.get("id")
    except requests.exceptions.HTTPError as e:
        raise e