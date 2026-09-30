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
        requests.RequestException: If the HTTP request fails or returns an unsuccessful status code.
    """
    base_url = "https://petstore.swagger.io/v2"
    order_url = f"{base_url}/store/order"
    
    payload = {
        "petId": inputs["new_pet_identifier"],
        "quantity": inputs["new_quantity"],
        "shipDate": None,  # Not provided in inputs; defaulting to null
        "status": "placed",  # Default status as per OpenAPI spec examples
        "complete": inputs["new_complete"]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(order_url, json=payload, headers=headers)
    
    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to place order: HTTP {response.status_code} - {response.text}")
    
    # Return None for successful empty response (e.g., 201 Created with no body)
    if response.content == b"":
        return None
    
    try:
        return response.json()
    except ValueError:
        raise Exception(f"Invalid JSON response from server: {response.text}")