import requests

def solve(inputs):
    """
    Fetches a purchase order by its ID from the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing 'order_identifier' (the ID of the order).
        
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, 
                      None if the response is empty but successful.
                      
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://petstore.swagger.io/v2"
    order_id = inputs.get("order_identifier")
    
    url = f"{base_url}/store/order/{order_id}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return None if not data else data
    elif response.status_code in (404, 500):
        raise Exception(f"Failed to fetch order {order_id}. Status code: {response.status_code}")
    else:
        raise requests.RequestException(f"HTTP error occurred: {response.status_code} - {response.text}")