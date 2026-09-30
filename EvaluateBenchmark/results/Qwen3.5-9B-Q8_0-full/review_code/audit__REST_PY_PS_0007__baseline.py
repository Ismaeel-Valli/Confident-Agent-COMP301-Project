import requests

def solve(inputs):
    """
    Deletes a pet from the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): A dictionary containing:
            - 'pet_identifier' (str): The ID of the pet to delete.
            - 'credential' (str): The API key or bearer token for authentication.
    
    Returns:
        int: The successful HTTP status code (e.g., 204).
    
    Raises:
        requests.RequestException: If the HTTP request fails or returns an unsuccessful status code.
    """
    pet_id = inputs['pet_identifier']
    credential = inputs['credential']
    
    # Base URL for Swagger Petstore OpenAPI 3 (Public Demo)
    base_url = "https://petstore3.swagger.io/api/v3"
    url = f"{base_url}/pet/{pet_id}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code >= 400:
        raise requests.RequestException(f"Failed to delete pet. Status code: {response.status_code}, Response: {response.text}")
    
    return response.status_code