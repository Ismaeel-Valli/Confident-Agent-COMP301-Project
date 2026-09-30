import requests

def solve(inputs):
    page = inputs.get('page')
    if page is None:
        raise ValueError("Missing 'page' in inputs")
    
    response = requests.get(f"https://dummyjson.com/products?page={page}")
    response.raise_for_status()
    
    data = response.json()
    
    return None if not data else data