import requests
from typing import Dict, Any, Optional

def solve(inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Places an order for a pet in the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing the following keys:
            - new_complete: value for the complete attribute
            - new_resource_id: value for the id attribute
            - new_pet_identifier: value for the pet Id attribute
            - new_quantity: value for the quantity attribute
            - new_shipDate: value for the ship Date attribute
            - new_status: value for the status attribute
    
    Returns:
        Optional[Dict[str, Any]]: The decoded JSON response if successful (empty), 
                                  or None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    # Construct the order payload
    order_payload = {
        "id": inputs["new_resource_id"],
        "petId": inputs["new_pet_identifier"],
        "quantity": inputs["new_quantity"],
        "shipDate": inputs["new_shipDate"],
        "status": inputs["new_status"],
        "complete": inputs["new_complete"]
    }
    
    # Base URL for Swagger Petstore (OpenAPI 3)
    base_url = "https://petstore.swagger.io/v2"
    order_endpoint = f"{base_url}/store/order"
    
    try:
        response = requests.post(order_endpoint, json=order_payload)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Return None for a successful empty response
        if not response.content:
            return None
        
        # Decode and return the JSON response
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")