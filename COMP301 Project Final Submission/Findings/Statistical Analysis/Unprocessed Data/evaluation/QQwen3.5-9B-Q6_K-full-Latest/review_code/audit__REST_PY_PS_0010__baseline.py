import requests
from typing import Dict, Any, Optional

def solve(inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Fetches a purchase order by its ID from the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing 'order_identifier' as the key.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        requests.exceptions.HTTPError: If the HTTP response is unsuccessful.
        KeyError: If 'order_identifier' is missing from inputs.
    """
    order_identifier = inputs.get('order_identifier')
    if order_identifier is None:
        raise KeyError("Missing required key 'order_identifier' in inputs")

    # Swagger Petstore OpenAPI 3 base URL (standard public version)
    base_url = "https://petstore.swagger.io/v2"
    
    url = f"{base_url}/store/order/{order_identifier}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data if data else None
    elif response.status_code == 404:
        # Assuming the prompt implies we should raise on unsuccessful, 
        # and 404 is technically unsuccessful for fetching a specific ID.
        response.raise_for_status()
    else:
        response.raise_for_status()

    return None