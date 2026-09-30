import requests

def solve(inputs):
    """
    Deletes a purchase order by identifier for the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing 'order_identifier' as the ID of the order to delete.
        
    Returns:
        int: The successful HTTP status code (e.g., 204).
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    order_identifier = inputs['order_identifier']
    
    # Base URL for Swagger Petstore API (OpenAPI 3)
    base_url = "https://petstore.swagger.io/v2"
    
    # Construct the endpoint for deleting a purchase order
    url = f"{base_url}/store/order/{order_identifier}"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:
        return response.status_code
    else:
        raise Exception(f"Failed to delete order. Status code: {response.status_code}, Response: {response.text}")