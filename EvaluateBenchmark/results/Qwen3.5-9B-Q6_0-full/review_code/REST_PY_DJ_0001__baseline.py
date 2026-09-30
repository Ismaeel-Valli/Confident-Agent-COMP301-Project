import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON API.
    
    Args:
        inputs (dict): A dictionary containing 'page' key for pagination.
        
    Returns:
        list or None: Decoded JSON response as a list, or None if the list is empty.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    # Extract page number from inputs, default to 1
    page = inputs.get('page', 1)
    
    # Construct the API URL for products with pagination
    url = f"https://dummyjson.com/products?page={page}"
    
    try:
        response = requests.get(url)
        
        # Raise an exception for unsuccessful HTTP responses (status code outside 200-299)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Extract the products list from the response
        products = data.get('products', [])
        
        # Return None for a successful empty response
        if not products:
            return None
            
        return products
        
    except requests.exceptions.RequestException as e:
        raise e