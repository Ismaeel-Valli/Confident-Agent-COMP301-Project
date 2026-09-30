import requests

def solve(inputs):
    """
    Places an order for a pet in the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - new_pet_identifier (str): The ID of the pet to order.
            - new_quantity (int): The quantity of the pet.
            - new_shipDate (str): The ship date in 'yyyy-MM-dd' format.
    
    Returns:
        str or None: The ID of the created order, or None if the response is empty but successful.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails with an unsuccessful status code.
    """
    base_url = "https://petstore.swagger.io/v2"
    url = f"{base_url}/store/order"
    
    payload = {
        "petId": inputs["new_pet_identifier"],
        "quantity": inputs["new_quantity"],
        "shipDate": inputs["new_shipDate"]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        return response.json().get("id")
    elif response.status_code == 200:
        # Some implementations might return 200 with an empty body or just a status
        if not response.text.strip():
            return None
        return response.json().get("id")
    else:
        raise requests.exceptions.RequestException(f"Failed to place order. Status code: {response.status_code}, Response: {response.text}")