import requests

def solve(inputs):
    """Delete a product by identifier from DummyJSON and return its title."""
    base_url = "https://dummyjson.com/products"
    resource_id = inputs["resource_id"]
    
    try:
        response = requests.delete(f"{base_url}/{resource_id}")
        response.raise_for_status()
        
        if response.status_code == 204:
            return None
        
        data = response.json()
        title = data.get("title")
        return title if title is not None else None
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")