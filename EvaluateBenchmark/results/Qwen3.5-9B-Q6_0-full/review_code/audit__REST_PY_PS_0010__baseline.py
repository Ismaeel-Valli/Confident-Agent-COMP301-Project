import requests
from typing import Optional, Dict, Any

def solve(inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Fetches a purchase order by its ID from the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing 'order_identifier' as the key.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    order_id = inputs.get('order_identifier')
    
    # Base URL for Swagger Petstore OpenAPI 3 service
    base_url = "https://petstore.swagger.io/v2"
    endpoint = f"{base_url}/store/order/{order_id}"
    
    try:
        response = requests.get(endpoint)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        if response.status_code == 200 and not response.text.strip():
            return None
            
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Failed to fetch order {order_id}: {e}") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed for order {order_id}: {e}") from e