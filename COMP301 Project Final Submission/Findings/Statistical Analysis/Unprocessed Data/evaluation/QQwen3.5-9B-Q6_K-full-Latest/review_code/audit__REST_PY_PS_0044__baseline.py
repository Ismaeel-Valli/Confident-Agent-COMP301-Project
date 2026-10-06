import requests
from typing import Optional, Dict, Any

def solve(inputs: Dict[str, Any]) -> Optional[int]:
    """
    Places an order for a pet in the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): A dictionary containing:
            - new_pet_identifier: The ID of the pet to order.
            - new_quantity: The quantity of the pet to order.
            - new_shipDate: The ship date for the order.
    
    Returns:
        int or None: The ID of the created order, or None if the response is empty but successful.
    
    Raises:
        requests.RequestException: If the HTTP request fails (non-successful status code).
    """
    base_url = "https://petstore.swagger.io/v2"
    url = f"{base_url}/store/order"
    
    payload = {
        "petId": inputs["new_pet_identifier"],
        "quantity": inputs["new_quantity"],
        "shipDate": inputs["new_shipDate"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code >= 400:
        raise requests.RequestException(f"Failed to place order. Status code: {response.status_code}, Response: {response.text}")
    
    try:
        data = response.json()
        return data.get("id")
    except ValueError:
        # If the response is not JSON but the status was successful (e.g., 204 No Content)
        if response.status_code == 204:
            return None
        raise requests.RequestException(f"Unexpected response format. Status code: {response.status_code}, Response: {response.text}")