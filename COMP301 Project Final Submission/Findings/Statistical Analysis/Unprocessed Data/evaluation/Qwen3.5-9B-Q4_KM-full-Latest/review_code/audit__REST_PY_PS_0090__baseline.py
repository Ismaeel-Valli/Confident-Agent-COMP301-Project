import requests
from typing import Any, Optional, Dict

def solve(inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Places an order for a pet using the Swagger Petstore (OpenAPI 3) API.
    
    Args:
        inputs (dict): A dictionary containing:
            - new_complete: value for the 'complete' attribute of the order
            - new_resource_id: value for the 'id' attribute of the order
            - new_pet_identifier: value for the 'petId' attribute in the request path
            - new_quantity: value for the 'quantity' attribute of the order
    
    Returns:
        Optional[Dict[str, Any]]: The decoded JSON response if successful (empty body returns None),
                                  or raises an exception on HTTP error.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails (non-2xx status).
    """
    
    base_url = "https://petstore.swagger.io/v2"
    url = f"{base_url}/store/order/{inputs['new_pet_identifier']}"
    
    payload = {
        "quantity": inputs["new_quantity"],
        "petId": inputs["new_pet_identifier"],  # Note: petId is typically required in the body for /store/order/{petId}
        "shipDate": None,  # Optional field, defaulting to null/omitted
        "status": "placed",  # Default status if not provided; can be adjusted based on requirements
        "complete": inputs["new_complete"]
    }
    
    # Remove optional fields with None values if desired, but keeping them as per typical OpenAPI examples
    # For strict adherence to the prompt's implied structure, we'll include only what's specified plus required ones.
    # However, 'petId' is usually part of the path in /store/order/{petId}, so it might be redundant in the body.
    # Let's adjust payload to match typical OpenAPI 3 Petstore spec for POST /store/order/{petId}:
    # Body typically requires: quantity, shipDate (optional), status (optional). 'complete' and 'id' are response fields.
    # But the prompt says: new_complete -> complete attribute; new_resource_id -> id attribute. 
    # This suggests we might be updating an existing order or the prompt implies these are body fields for creation.
    # Given ambiguity, we'll construct the payload as if creating a new order with provided attributes in the body.
    
    # Re-evaluating: The endpoint /store/order/{petId} usually takes quantity and status in the body.
    # 'id' and 'complete' are typically set by the server upon creation. 
    # However, the prompt explicitly maps inputs to these attributes. To strictly follow instructions:
    
    payload = {
        "quantity": inputs["new_quantity"],
        "complete": inputs["new_complete"],
        "id": inputs["new_resource_id"]  # Some implementations might allow setting this, though unusual for creation
    }
    # We omit 'petId' in the body since it's in the URL path.
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200 or response.status_code == 201:
        # Successful creation/update; return None for empty body (201 often returns empty JSON object {})
        if not response.text.strip():
            return None
        else:
            try:
                return response.json()
            except ValueError:
                return None
    else:
        raise requests.exceptions.RequestException(
            f"Failed to place order. Status code: {response.status_code}, Response: {response.text}"
        )