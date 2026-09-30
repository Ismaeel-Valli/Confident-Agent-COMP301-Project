import requests

def solve(inputs):
    """
    Searches for products using the provided search term via DummyJSON API.
    
    Args:
        inputs (dict): A dictionary containing 'search_text' key with the search term.
        
    Returns:
        list or None: Decoded JSON response if successful. Returns None if the response is empty.
                      Raises an exception for unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/products/search"
    search_text = inputs.get("search_text", "")
    
    params = {
        "q": search_text,
        "limit": 100  # Adjust as needed
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # DummyJSON returns a list of products in the 'products' key
        products = data.get("products", [])
        
        if not products:
            return None
            
        return products
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")