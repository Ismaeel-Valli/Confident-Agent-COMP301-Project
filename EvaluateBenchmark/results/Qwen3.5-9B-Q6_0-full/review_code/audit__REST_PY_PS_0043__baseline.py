import requests

def solve(inputs):
    """
    Updates a pet in the store with form data for Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): A dictionary containing:
            - 'pet_identifier': ID of the pet to update.
            - 'status': New status for the pet.
            - 'credential': Caller-supplied credential (e.g., API key or token).
    
    Returns:
        int or None: The response's status code, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful request.
    """
    base_url = "https://petstore.swagger.io/v2"
    url = f"{base_url}/pet/{inputs['pet_identifier']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "status": inputs['status']
    }
    
    response = requests.put(url, headers=headers, data=data)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update pet: HTTP {response.status_code} - {response.text}")
    
    return response.status_code if response.content else None