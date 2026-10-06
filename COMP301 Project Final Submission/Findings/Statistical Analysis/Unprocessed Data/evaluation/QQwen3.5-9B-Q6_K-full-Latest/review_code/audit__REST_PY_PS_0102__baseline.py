import requests

def solve(inputs):
    """
    Places an order for a pet in the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - new_pet_identifier (str): The ID of the pet to order.
            - new_quantity (int): The quantity of the pet to order.
            - new_shipDate (str): The ship date in 'yyyy-MM-dd' format.
            - new_status (str): The status of the order (e.g., 'placed', 'approved', 'delivered').
    
    Returns:
        str or None: The ID of the created order, or None if the response is empty but successful.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    # Base URL for Swagger Petstore OpenAPI 3
    base_url = "https://petstore.swagger.io/v2"
    
    # Construct the order payload
    order_data = {
        "petId": inputs["new_pet_identifier"],
        "quantity": inputs["new_quantity"],
        "shipDate": inputs["new_shipDate"],
        "status": inputs["new_status"]
    }
    
    # Endpoint to place an order
    url = f"{base_url}/store/order"
    
    try:
        response = requests.post(url, json=order_data)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Return the ID from the response JSON if present
        if response.status_code == 200 and response.json():
            return response.json().get("id")
        elif response.status_code == 201:
            # For created resources, the ID might be in the Location header or response body
            location = response.headers.get("Location")
            if location:
                # Extract ID from URL if possible (e.g., /store/order/123)
                parts = location.split("/")
                for part in reversed(parts):
                    if part.isdigit():
                        return int(part)
            # If no Location header and empty body, return None as per instructions
            return None
        else:
            # Fallback for other successful status codes with empty response
            return None
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Failed to place order: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")