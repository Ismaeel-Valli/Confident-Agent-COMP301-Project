import requests

def solve(inputs):
    """Submit a new product to DummyJSON and return its id, or None if absent."""
    base_url = "https://dummyjson.com/products"
    url = f"{base_url}/add"
    
    payload = {
        "title": inputs["new_title"],
        "category": inputs["new_category"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 201:
        data = response.json()
        return data.get("id")
    elif response.status_code == 200:
        # Some APIs return empty body on success
        return None
    else:
        raise Exception(f"Failed to submit product: HTTP {response.status_code}")