import requests
from typing import Any, Dict, Optional

def solve(inputs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Places an order for a pet using the Swagger Petstore (OpenAPI 3) API.
    
    Args:
        inputs: A dictionary containing:
            - new_complete: value for the 'complete' attribute of the order
            - new_resource_id: value for the 'id' attribute of the order
            - new_pet_identifier: value for the 'petId' attribute in the request body
            - new_quantity: value for the 'quantity' attribute of the order
    
    Returns:
        The decoded JSON response if successful, or None for an empty successful response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code >= 400).
    """
    # Construct the order payload based on the inputs provided
    order_payload = {
        "petId": inputs["new_pet_identifier"],
        "quantity": inputs["new_quantity"],
        "shipDate": None,  # Optional field, not specified in inputs
        "status": "placed",  # Default status as per OpenAPI spec examples
        "complete": inputs["new_complete"]
    }

    # Base URL for Swagger Petstore API (using the public demo server)
    base_url = "https://petstore.swagger.io/v2"
    
    # Endpoint to place an order
    url = f"{base_url}/store/order"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.post(url, json=order_payload, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Return the decoded JSON response
        if response.status_code == 201:  # Created
            return None  # Successful empty response as per instruction
        elif response.status_code == 200:  # OK (might happen in some implementations)
            return response.json()
        else:
            # This should not be reached due to raise_for_status(), but for safety
            raise Exception(f"Unexpected successful status code: {response.status_code}")
            
    except requests.exceptions.HTTPError as e:
        # Re-raise the exception with additional context if needed
        raise Exception(f"Failed to place order: {e.response.text if e.response else 'No response text'}") from e
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}") from e