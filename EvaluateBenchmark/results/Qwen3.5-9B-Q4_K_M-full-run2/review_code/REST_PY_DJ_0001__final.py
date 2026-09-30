def solve(inputs):
    """Retrieve one page of products from DummyJSON and return decoded JSON."""
    import requests
    
    base_url = inputs.get("base_url", "https://dummyjson.com/products")
    page = inputs.get("page", 1)
    
    url = f"{base_url}?skip=0&limit=10&page={page}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data if data else None
    else:
        raise Exception(f"HTTP {response.status_code}: Failed to retrieve products")