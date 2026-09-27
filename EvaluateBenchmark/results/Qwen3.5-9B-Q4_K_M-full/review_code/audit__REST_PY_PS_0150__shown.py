def solve(inputs):
    """
    Place an order for a pet using Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Dictionary containing:
            - new_complete: value for the complete attribute
            - new_resource_id: value for the id attribute
            - new_pet_identifier: value for the pet Id attribute
            - new_quantity: value for the quantity attribute
            - new_shipDate: value for the ship Date attribute
            - new_status: value for the status attribute
    
    Returns:
        int or None: The response's id value, or None if absent. Returns None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    import requests
    
    # Swagger Petstore base URL (OpenAPI 3 service) - use /api/v3 as declared in OpenAPI spec
    base_url = "https://petstore3.swagger.io/api"
    
    # Build the order payload from inputs
    order_payload = {
        "complete": inputs["new_complete"],
        "id": inputs["new_resource_id"],
        "petId": inputs["new_pet_identifier"],
        "quantity": inputs["new_quantity"],
        "shipDate": inputs["new_shipDate"],
        "status": inputs["new_status"]
    }
    
    # Place the order using POST to /store/order endpoint
    response = requests.post(f"{base_url}/v3/store/order", json=order_payload)
    
    # Raise exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Parse the response JSON
    try:
        result = response.json()
    except ValueError:
        return None
    
    # Return id if present, otherwise None
    if "id" in result:
        return result["id"]
    else:
        return None