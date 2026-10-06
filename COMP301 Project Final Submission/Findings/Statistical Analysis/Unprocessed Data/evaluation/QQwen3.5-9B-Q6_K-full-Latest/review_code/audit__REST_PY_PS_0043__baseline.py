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
    pet_id = inputs['pet_identifier']
    new_status = inputs['status']
    credential = inputs['credential']

    # Prepare headers with the provided credential (assuming it's an API key or similar)
    headers = {
        "Authorization": f"Bearer {credential}" if credential.startswith("Bearer ") else f"{credential}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Prepare form data
    data = {
        "status": new_status
    }

    try:
        response = requests.put(
            f"{base_url}/pet/{pet_id}",
            headers=headers,
            data=data
        )
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Return status code if present, otherwise None
        return getattr(response, 'status_code', None)
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")