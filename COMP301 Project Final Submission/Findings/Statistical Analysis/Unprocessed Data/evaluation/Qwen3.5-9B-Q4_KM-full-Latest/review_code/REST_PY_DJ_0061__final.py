def solve(inputs):
    """Retrieve one page of products from DummyJSON, filtering fields as specified."""
    import requests
    
    base_url = "https://dummyjson.com/products"
    
    included_fields = inputs.get("included_fields", "")
    if included_fields:
        field_list = [f.strip() for f in included_fields.split(",")]
        url = f"{base_url}?limit=1&fields={','.join(field_list)}"
    else:
        url = f"{base_url}?limit=1"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    return response.json()