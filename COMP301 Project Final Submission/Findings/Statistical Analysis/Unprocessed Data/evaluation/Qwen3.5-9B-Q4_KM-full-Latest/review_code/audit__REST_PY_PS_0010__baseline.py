import requests

def solve(inputs):
    """
    Fetches a purchase order by ID from the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing 'order_identifier' as the order ID.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    order_identifier = inputs['order_identifier']
    
    # Swagger Petstore base URL (using the public demo server)
    url = "https://petstore3.swagger.io/api/v3/pet"
    
    # Note: The standard Swagger Petstore OpenAPI 3 example does not have a direct '/orders/{orderId}' endpoint 
    # in the public demo version. However, based on common REST patterns and the request to find an order by ID,
    # we will assume a hypothetical endpoint structure often found in such services or use a known orders endpoint if available.
    # Since the public Swagger Petstore v3 does not expose an 'orders' collection in its standard demo, 
    # this function assumes a custom or extended service where '/orders/{orderId}' exists.
    
    # Constructing the URL for fetching a specific order by ID
    fetch_url = f"https://petstore3.swagger.io/api/v3/orders/{order_identifier}"
    
    try:
        response = requests.get(fetch_url)
        
        if response.status_code == 200:
            data = response.json()
            # Return None for an empty response (though unlikely for a specific ID fetch, it's per requirement)
            return data if data else None
        elif response.status_code == 404:
            # If the order is not found, we might return None or raise depending on strictness. 
            # The prompt says "Raise an exception for an unsuccessful HTTP response". 
            # 404 is technically unsuccessful in this context if we expect it to exist.
            raise Exception(f"Order with ID {order_identifier} not found.")
        else:
            raise Exception(f"Failed to fetch order. Status code: {response.status_code}, Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error occurred while fetching the order: {str(e)}")