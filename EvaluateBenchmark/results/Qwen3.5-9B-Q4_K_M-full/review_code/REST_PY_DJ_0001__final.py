import requests

def solve(inputs):
    """Retrieve one page of products from DummyJSON and return decoded JSON."""
    base_url = inputs.get("base_url", "https://dummyjson.com/products")
    page = inputs.get("page", 1)
    
    url = f"{base_url}?skip=0&limit=5&page={page}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data