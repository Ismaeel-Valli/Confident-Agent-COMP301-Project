import requests

def solve(inputs):
    """
    Updates a pet in the store with form data for Swagger Petstore (OpenAPI 3).
    
    Args:
        inputs (dict): A dictionary containing:
            - 'pet_identifier' (str): ID of the pet to update.
            - 'status' (str): New status of the pet.
            - 'credential' (str): Bearer token for authentication.
    
    Returns:
        int or None: The response's status code, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response indicates an error.
    """
    base_url = "https://petstore.swagger.io/v2"
    pet_id = inputs['pet_identifier']
    status = inputs['status']
    credential = inputs['credential']
    
    url = f"{base_url}/pet/{pet_id}"
    headers = {
        'Authorization': f'Bearer {credential}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'status': status
    }
    
    response = requests.put(url, headers=headers, data=data)
    
    if response.status_code >= 400:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    # Return None for successful empty responses (e.g., 204 No Content)
    if response.status_code == 204 or (response.status_code == 200 and not response.content):
        return None
    
    return response.status_code