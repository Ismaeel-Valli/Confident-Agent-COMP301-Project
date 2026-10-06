import requests

def solve(inputs):
    """
    Places an order for a pet in the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): A dictionary containing:
            - new_pet_identifier (str): The ID of the pet to order.
            - new_quantity (int): The quantity of the pet.
            - new_shipDate (str): The ship date in 'yyyy-MM-dd' format.
    
    Returns:
        str or None: The response's id value if present, otherwise None for a successful empty response.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code indicates an error.
    """
    base_url = "https://petstore.swagger.io/v2"
    order_endpoint = f"{base_url}/store/order"
    
    payload = {
        "petId": inputs["new_pet_identifier"],
        "quantity": inputs["new_quantity"],
        "shipDate": inputs["new_shipDate"]
    }
    
    response = requests.post(order_endpoint, json=payload)
    response.raise_for_status()
    
    if response.status_code == 201:
        return response.json().get("id")
    elif response.status_code == 204:
        return None
    
    # If we get here, it's an unexpected success code or a logic error in the API spec interpretation
    # But per instructions, we only raise on unsuccessful HTTP responses.
    # Assuming 201 and 204 are the only successful ones for this endpoint.
    return None