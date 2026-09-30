import requests

def solve(inputs):
    """Delete a product by identifier from DummyJSON and return isDeleted or None."""
    resource_id = inputs.get("resource_id")
    if resource_id is None:
        raise ValueError("Missing required 'resource_id' in inputs")
    
    url = f"https://dummyjson.com/products/{resource_id}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {"id": resource_id}
    
    try:
        response = requests.delete(url, json=payload, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 200:
            # Successful deletion with empty response
            return None
        
        data = response.json()
        
        if "isDeleted" in data:
            return data["isDeleted"]
        else:
            return None
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")