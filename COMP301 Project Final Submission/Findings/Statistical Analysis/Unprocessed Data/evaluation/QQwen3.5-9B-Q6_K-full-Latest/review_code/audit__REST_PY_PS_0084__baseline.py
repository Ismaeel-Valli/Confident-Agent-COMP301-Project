import requests

def solve(inputs):
    """
    Places an order for a pet in the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - new_resource_id: Value for the 'id' attribute of the order.
            - new_pet_identifier: Value for the 'petId' attribute.
            - new_quantity: Value for the 'quantity' attribute.
            - new_status: Value for the 'status' attribute.
    
    Returns:
        int or None: The 'id' value from the response, or None if absent or successful empty response.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request is unsuccessful.
    """
    # Base URL for Swagger Petstore API (using public demo instance)
    base_url = "https://petstore.swagger.io/v2"
    
    # Construct the order payload
    order_payload = {
        "petId": inputs["new_pet_identifier"],
        "quantity": inputs["new_quantity"],
        "shipDate": None,  # Optional field, not provided in inputs
        "status": inputs["new_status"],
        "complete": False  # Optional field, defaulting to False
    }

    try:
        response = requests.post(
            f"{base_url}/store/order",
            json=order_payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Check if the response is empty (no content)
        if not response.text:
            return None
        
        # Parse the JSON response to extract the 'id' attribute
        try:
            response_data = response.json()
            return response_data.get("id")
        except ValueError:
            # If the response is not valid JSON, return None as per instructions for successful empty response
            return None
            
    except requests.exceptions.HTTPError as e:
        raise e
    except requests.exceptions.RequestException as e:
        raise e