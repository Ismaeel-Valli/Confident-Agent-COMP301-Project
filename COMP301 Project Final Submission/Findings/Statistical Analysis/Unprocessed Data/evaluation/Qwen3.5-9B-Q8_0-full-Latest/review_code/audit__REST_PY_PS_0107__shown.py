def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Dictionary containing:
            - credential (str): Caller-supplied authentication token.
            - new_resource_id (int): Value for the 'id' attribute.
            - new_name (str): Value for the 'name' attribute.
            - new_photo_links (list of str): Value for the 'photoUrls' attribute.
            - new_tags (list of dict): Value for the 'tags' attribute.
    
    Returns:
        int or None: The response's status code, or None if absent.
                     For a successful empty response, returns None.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    import requests
    
    # Swagger Petstore base URL with /api/v3 path as per OpenAPI spec
    base_url = "https://petstore3.swagger.io/api/v3"
    
    # Prepare the payload for the new pet
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "tags": inputs["new_tags"]
    }
    
    # Set up headers with the credential for authentication
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    # Endpoint to add a new pet (POST /pet)
    url = f"{base_url}/pet"
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Return the status code if present, otherwise None
        if "status" in response.json():
            return response.json()["status"]
        else:
            # For a successful empty response, return None
            return None
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")