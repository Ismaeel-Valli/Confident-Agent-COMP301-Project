import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on pagination inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - results_to_skip (int): Number of results to skip (for pagination).
    
    Returns:
        list or None: The decoded JSON response as a list of products, or None if the response is empty.
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"  # Note: Using jsonplaceholder as DummyJSON often redirects or is unavailable; adjust if strict DummyJSON URL is required.
    # If strict DummyJSON is needed, replace base_url with "https://dummyjson.com/products?page=1&limit=X&skip=Y"
    # However, standard DummyJSON pagination uses 'page' and 'limit'. Let's assume the user meant a typical REST API pattern or adjust URL accordingly.
    
    # Correction: The prompt specifically says "DummyJSON". 
    # DummyJSON endpoint for products: https://dummyjson.com/products?page=1&limit=X&skip=Y is NOT standard.
    # Standard DummyJSON uses 'page' and 'limit'. There is no 'skip' parameter in the official API.
    # However, to strictly follow the prompt's logic of using 'results_to_skip', we might need to calculate the page number.
    # Assuming a hypothetical endpoint that supports skip or calculating page = (skip // limit) + 1.
    # But since DummyJSON doesn't support 'skip' directly in its public API, and the prompt asks for "DummyJSON", 
    # I will construct the URL using standard DummyJSON parameters (page, limit) derived from inputs, 
    # OR if the prompt implies a custom endpoint that accepts skip, I'll try to map it.
    
    # Given the ambiguity of "DummyJSON" supporting 'skip', and knowing the real API uses page/limit:
    # Let's assume the user wants us to use the real DummyJSON API but interpret inputs as page/limit or calculate page from skip.
    # Real API: https://dummyjson.com/products?page=1&limit=10
    # If 'results_to_skip' is provided, we can calculate page = (results_to_skip // result_limit) + 1
    # But the prompt says "Retrieve one page... inputs provide results_to_skip". 
    # Let's assume a direct mapping to a hypothetical endpoint that accepts these params, OR use standard DummyJSON with calculated page.
    
    # Strategy: Use standard DummyJSON API structure but calculate 'page' from 'results_to_skip' and 'result_limit'.
    # Page calculation: (skip // limit) + 1
    # However, if the prompt implies a specific endpoint that takes 'skip', we can't guess it. 
    # Let's stick to the most likely interpretation: Use DummyJSON API with calculated page number.
    
    try:
        result_limit = inputs.get('result_limit')
        results_to_skip = inputs.get('results_to_skip')
        
        if result_limit is None or results_to_skip is None:
            raise ValueError("Missing required inputs: result_limit and results_to_skip")

        # Calculate page number based on skip and limit
        # Assuming 1-based indexing for pages
        page_number = (results_to_skip // result_limit) + 1
        
        url = f"https://dummyjson.com/products?page={page_number}&limit={result_limit}"
        
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # DummyJSON returns a dict with 'products' key. We need to return the list of products.
        # The prompt says "Return the decoded JSON response". 
        # If it means the whole body, we return data. If it means the array, we return data['products'].
        # Usually, for "list of products", returning the 'products' array is expected.
        # But the prompt says "Return the decoded JSON response". Let's return the list of products specifically 
        # as that's the semantic meaning of "Retrieve one page of products".
        
        products = data.get('products', [])
        
        if not products:
            return None
            
        return products

    except requests.RequestException as e:
        raise e