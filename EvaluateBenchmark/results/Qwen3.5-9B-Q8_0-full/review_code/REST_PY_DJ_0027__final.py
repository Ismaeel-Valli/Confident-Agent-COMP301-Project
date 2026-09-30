import requests

def solve(inputs):
    """Delete a product by identifier from DummyJSON and return its id."""
    resource_id = inputs.get("resource_id")
    
    if resource_id is None:
        return None
    
    url = "https://dummyjson.com/products/{id}".format(id=resource_id)
    
    try:
        response = requests.delete(url)
        response.raise_for_status()
        
        data = response.json()
        
        # DummyJSON delete returns {"success": true, "message": "..."} on success
        if data.get("success") is True:
            return None
        
        # If the attribute 'id' is present in the response, return it
        if "id" in data:
            return data["id"]
        
        return None
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")