import requests

def solve(inputs):
    """
    Updates a pet in the Swagger Petstore (OpenAPI 3) store with form data.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'pet_identifier': The ID of the pet to update.
            - 'status': The new status for the pet.
            - 'credential': Caller-supplied credential (e.g., API key or token).
    
    Returns:
        int or None: The response's status code, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status.
    """
    pet_identifier = inputs['pet_identifier']
    status = inputs['status']
    credential = inputs['credential']

    # Base URL for Swagger Petstore (OpenAPI 3) - using a standard public instance for demonstration
    base_url = "https://petstore.swagger.io/v2"
    
    # Construct the update endpoint URL
    url = f"{base_url}/pet/{pet_identifier}"
    
    # Prepare form data as per OpenAPI 3 spec for PUT /pet with form data
    payload = {
        'status': status
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.put(url, data=payload, headers=headers, auth=('user', credential))
        
        # Check if the response is successful (2xx)
        if 200 <= response.status_code < 300:
            # If the response content is empty, return None as per instructions
            if not response.text.strip():
                return None
            return response.status_code
        
        # Raise an exception for unsuccessful HTTP responses
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    except requests.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")