import requests
from typing import Any, Dict, Optional

def solve(inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Fetches a purchase order by its ID from the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing 'order_identifier' as the key.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        requests.RequestException: If the HTTP request is unsuccessful.
    """
    order_id = inputs.get('order_identifier')
    
    if not order_id:
        raise ValueError("Missing 'order_identifier' in inputs.")

    url = "https://petstore.swagger.io/v2/order"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, params={"orderId": order_id}, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 204 or not response.text.strip():
            return None
            
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Failed to fetch order {order_id}: {e}") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed for order {order_id}: {e}") from e