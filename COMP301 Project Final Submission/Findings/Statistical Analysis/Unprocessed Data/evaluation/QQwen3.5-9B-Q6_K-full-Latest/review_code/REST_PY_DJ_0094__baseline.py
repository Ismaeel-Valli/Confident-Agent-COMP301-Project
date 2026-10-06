import requests

def solve(inputs):
    """
    Updates selected fields of a product in DummyJSON.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (int): Identifier of the product.
            - new_price (float): New value for the price attribute.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, 
                      None if the response is empty (204 No Content).
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    resource_id = inputs['resource_id']
    new_price = inputs['new_price']
    
    # Base URL for DummyJSON API
    base_url = "https://dummyjson.com/products"
    
    # Construct the update payload
    payload = {
        "id": resource_id,
        "price": new_price
    }
    
    try:
        response = requests.put(
            f"{base_url}/{resource_id}",
            json=payload,
            timeout=10
        )
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Return None for a successful empty response (204 No Content)
        if response.status_code == 204:
            return None
        
        # Decode and return the JSON response
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}") from e
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}") from e