import requests

def solve(inputs):
    """
    Retrieves one page of products from DummyJSON based on sort field and direction.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'sort_field' (str): The field to sort by.
            - 'sort_direction' (str): The sorting direction ('asc' or 'desc').
    
    Returns:
        list or None: The decoded JSON response as a list of products, or None if the response is empty.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://dummyjson.com/products"
    
    # Construct query parameters
    params = {
        'sort': inputs['sort_field'],
        'order': inputs['sort_direction']
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Return the products list if it exists and is not empty
        if data.get('products'):
            return data['products']
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        raise e