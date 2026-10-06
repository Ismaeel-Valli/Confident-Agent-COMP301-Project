import requests

def solve(inputs):
    """Submit a new product to DummyJSON."""
    base_url = "https://dummyjson.com/products"
    url = f"{base_url}/add"
    
    payload = {
        "title": inputs["new_title"],
        "price": inputs["new_price"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to add product. Status code: {response.status_code}")
    
    return None