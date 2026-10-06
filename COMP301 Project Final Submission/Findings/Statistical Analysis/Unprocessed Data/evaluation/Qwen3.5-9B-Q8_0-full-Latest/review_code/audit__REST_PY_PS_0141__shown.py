def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Inputs:
        - new_name: value for the name attribute
        - new_photo_links: value for the photoUrls attribute
        - new_status: value for the status attribute
        - new_tags: value for the tags attribute
        - credential: caller-supplied credential (assumed to have necessary permissions)
    
    Returns:
        The response's 'name' value, or None if that attribute is absent.
        Returns None for a successful empty response.
        Raises an exception for an unsuccessful HTTP response.
    """
    import requests
    
    # Base URL for Swagger Petstore (OpenAPI 3) - includes the /api/v3 path from OpenAPI spec
    base_url = "https://petstore3.swagger.io/api/v3"
    
    # Prepare the payload for adding a new pet
    payload = {
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"],
        "tags": inputs["new_tags"]
    }
    
    # Use Bearer token authentication with the provided credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    # Endpoint to add a new pet (POST /pet)
    url = f"{base_url}/pet"
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Return the 'name' value from the response, or None if absent
        return response.json().get("name")
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Failed to add pet: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")