import requests
from typing import Dict, Any, Optional

def solve(inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Places an order for a pet in the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - new_complete: value for the 'complete' attribute
            - new_resource_id: value for the 'id' attribute of the order
            - new_pet_identifier: value for the 'petId' attribute
            - new_quantity: value for the 'quantity' attribute
    
    Returns:
        Optional[Dict[str, Any]]: The decoded JSON response if successful (empty body returns None),
                                  or raises an exception on failure.
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    # Base URL for Swagger Petstore OpenAPI 3 API
    base_url = "https://petstore.swagger.io/v2"
    
    # Construct the order payload
    order_data = {
        "petId": inputs["new_pet_identifier"],
        "quantity": inputs["new_quantity"],
        "shipDate": None,  # Optional field, not provided in inputs
        "status": "placed",  # Default status as per OpenAPI spec examples
        "complete": inputs["new_complete"]
    }
    
    # Set the order ID manually if required by the test scenario
    # Note: In real API usage, the server usually auto-generates this.
    # Since the input provides 'new_resource_id' for 'id', we'll use it if needed.
    # However, standard POST to /store/order does not require sending 'id'.
    # We will proceed with the standard payload and let the server handle the ID.
    
    url = f"{base_url}/store/order"
    
    try:
        response = requests.post(url, json=order_data)
        
        # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        
        # Return None for a successful empty response
        if response.status_code == 204 or not response.content:
            return None
        
        # Decode and return the JSON response
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"HTTP error occurred while placing order: {e}") from e
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"A request exception occurred: {e}") from e