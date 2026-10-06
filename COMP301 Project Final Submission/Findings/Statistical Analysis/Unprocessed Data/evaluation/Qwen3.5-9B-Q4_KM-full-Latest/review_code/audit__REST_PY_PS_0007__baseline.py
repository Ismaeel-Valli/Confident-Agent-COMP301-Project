import requests

def solve(inputs):
    """
    Deletes a pet from the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'pet_identifier' (str): The ID of the pet to delete.
            - 'credential' (dict): Caller-supplied credentials (e.g., {'api_key': '...', 'bearer_token': '...'}).
    
    Returns:
        int: The successful HTTP status code (typically 200 or 204).
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful operation.
    """
    base_url = "https://petstore.swagger.io/v2"
    pet_id = inputs["pet_identifier"]
    credentials = inputs["credential"]

    # Construct headers based on common Swagger Petstore authentication methods
    # Note: The exact method (API Key vs Bearer Token) depends on the specific implementation.
    # We'll try a generic approach often used in OpenAPI 3 examples.
    headers = {
        "Content-Type": "application/json"
    }

    if "api_key" in credentials:
        headers["x-api-key"] = credentials["api_key"]
    elif "bearer_token" in credentials:
        headers["Authorization"] = f"Bearer {credentials['bearer_token']}"

    url = f"{base_url}/pet/{pet_id}"
    response = requests.delete(url, headers=headers)

    if response.status_code == 200 or response.status_code == 204:
        return response.status_code
    else:
        raise Exception(f"Failed to delete pet. Status code: {response.status_code}, Response: {response.text}")