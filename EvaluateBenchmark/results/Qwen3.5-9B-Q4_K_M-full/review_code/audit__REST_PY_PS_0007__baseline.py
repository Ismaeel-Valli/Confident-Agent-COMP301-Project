import requests

def solve(inputs):
    """
    Deletes a pet from the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): A dictionary containing:
            - 'pet_identifier': The ID of the pet to delete.
            - 'credential': Caller-supplied credential (e.g., API key or token) for authentication.
    
    Returns:
        int: The successful HTTP status code (typically 200 or 204).
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful operation.
    """
    pet_id = inputs["pet_identifier"]
    credential = inputs["credential"]
    
    # Base URL for Swagger Petstore OpenAPI 3 (public demo server)
    base_url = "https://petstore3.swagger.io/api/v3"
    
    # Construct the delete endpoint URL
    url = f"{base_url}/pet/{pet_id}"
    
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": credential  # Assuming API key is used for authentication
    }
    
    response = requests.delete(url, headers=headers)
    
    if response.status_code in [200, 204]:
        return response.status_code
    else:
        raise Exception(f"Failed to delete pet. Status code: {response.status_code}, Response: {response.text}")