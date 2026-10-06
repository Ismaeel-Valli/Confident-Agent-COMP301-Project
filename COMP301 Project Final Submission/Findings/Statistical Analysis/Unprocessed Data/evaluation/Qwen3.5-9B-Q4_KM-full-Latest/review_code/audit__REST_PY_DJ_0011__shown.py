import requests

def solve(inputs):
    """Search users on DummyJSON using a search term."""
    base_url = "https://dummyjson.com/users/search"
    url = f"{base_url}?q={inputs['search_text']}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get('users'):
            return None
        
        return data
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")