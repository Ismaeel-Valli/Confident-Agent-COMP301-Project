import requests

def solve(inputs):
    """Submit a new product to DummyJSON and return its title, or None if absent."""
    base_url = "https://dummyjson.com/products/add"
    
    payload = {
        "title": inputs["new_title"],
        "description": inputs["new_description"]
    }
    
    response = requests.post(base_url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create product. Status code: {response.status_code}")
    
    data = response.json()
    
    # DummyJSON returns the created product in the response body for POST /products/add
    title = data.get("title")
    
    return title if title is not None else None