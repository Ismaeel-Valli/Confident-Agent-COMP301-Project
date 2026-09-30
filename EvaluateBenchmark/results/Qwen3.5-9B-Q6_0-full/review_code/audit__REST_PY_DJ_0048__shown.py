def solve(inputs):
    """Submit a new product to DummyJSON and return its title."""
    import requests
    
    base_url = "https://dummyjson.com/products"
    url = f"{base_url}/add"
    
    try:
        response = requests.post(url, json={"title": inputs["new_title"]})
        response.raise_for_status()
        
        if response.status_code == 201:
            data = response.json()
            return data.get("title")
        elif response.status_code == 200:
            # Some endpoints return empty body on success
            return None
        else:
            raise Exception(f"Failed to create product. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")