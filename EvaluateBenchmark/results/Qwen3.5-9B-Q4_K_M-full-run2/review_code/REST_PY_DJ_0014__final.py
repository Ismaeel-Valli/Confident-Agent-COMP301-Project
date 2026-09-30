import requests

def solve(inputs):
    """Retrieve a post by identifier from DummyJSON."""
    base_url = "https://dummyjson.com/posts"
    resource_id = inputs["resource_id"]
    
    try:
        response = requests.get(f"{base_url}/{resource_id}")
        
        if response.status_code == 200:
            data = response.json()
            # DummyJSON returns {"post": {...}} on success
            return data["post"]
        elif response.status_code == 404:
            # No post found - treat as empty successful response
            return None
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed: {e}")