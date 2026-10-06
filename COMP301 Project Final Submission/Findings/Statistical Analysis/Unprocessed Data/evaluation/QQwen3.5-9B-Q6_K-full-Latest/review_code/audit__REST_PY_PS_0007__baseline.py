import requests

def solve(inputs):
    """
    Deletes a pet from the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): A dictionary containing:
            - 'pet_identifier' (str): The ID of the pet to delete.
            - 'credential' (str): The bearer token for authentication.
    
    Returns:
        int: The successful HTTP status code (typically 204).
    
    Raises:
        requests.exceptions.RequestException: If the request fails or returns an unsuccessful status code.
    """
    base_url = "https://petstore3.swagger.io/api/v3/openapi"
    pet_id = inputs['pet_identifier']
    credential = inputs['credential']
    
    url = f"{base_url}/pet/{pet_id}"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to delete pet. Status code: {response.status_code}, Response: {response.text}")
    
    return response.status_code