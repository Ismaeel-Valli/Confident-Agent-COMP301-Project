import requests

def solve(inputs):
    """Submit a new product to DummyJSON."""
    base_url = "https://dummyjson.com/products"
    url = f"{base_url}/add"
    
    payload = {
        "description": inputs["new_description"],
        "title": inputs["new_title"]
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    data = response.json()
    
    if data.get("success"):
        return None
    
    raise Exception(f"Failed to submit product: {data}")