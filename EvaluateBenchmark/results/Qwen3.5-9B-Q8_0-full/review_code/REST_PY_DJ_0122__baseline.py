import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on skip count and sort field.
    
    Args:
        inputs (dict): A dictionary containing:
            - results_to_skip (int): Number of results to skip.
            - sort_field (str): Field used for ordering.
            
    Returns:
        list or None: The decoded JSON response as a list, or None if the response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"  # Note: Using jsonplaceholder as DummyJSON often redirects or isn't available for this specific pattern without auth. 
    # However, strictly following "DummyJSON" usually implies https://dummyjson.com/products
    
    url = "https://dummyjson.com/products"
    
    params = {
        "skip": inputs.get("results_to_skip", 0),
        "limit": 1,  # Retrieve one page (one item)
        "sort_by": inputs.get("sort_field")
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # DummyJSON structure for products list is usually under 'products' key
        if 'products' in data and len(data['products']) == 0:
            return None
            
        return data['products']
        
    except requests.RequestException as e:
        raise e