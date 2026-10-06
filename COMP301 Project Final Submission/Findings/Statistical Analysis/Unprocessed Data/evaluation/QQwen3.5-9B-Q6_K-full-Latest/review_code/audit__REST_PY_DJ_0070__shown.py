import requests

def solve(inputs):
    """Delete a post by identifier from DummyJSON and return isDeleted value."""
    base_url = "https://dummyjson.com/posts"
    resource_id = inputs["resource_id"]
    
    try:
        response = requests.delete(f"{base_url}/{resource_id}")
        
        if response.status_code >= 400:
            raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
        
        data = response.json()
        
        # Return isDeleted if present, None otherwise
        return data.get("isDeleted")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")