import requests

def solve(inputs):
    """
    Updates an existing pet in the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - new_resource_id (int): The ID of the pet to update.
            - new_name (str): The new name for the pet.
            - new_photo_links (list): List of photo URLs for the pet.
            - new_status (str): The new status of the pet.
            - new_tags (list): List of tags for the pet.
            - credential (dict or str): Credentials for authentication (assumed to have necessary permissions).
    
    Returns:
        int or None: The ID of the updated pet, or None if the response is empty/successful without an ID.
    
    Raises:
        Exception: If the HTTP response indicates failure.
    """
    # Base URL for Swagger Petstore OpenAPI 3 (assuming standard public instance)
    base_url = "https://petstore.swagger.io/v2"
    
    # Prepare the payload
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"],
        "tags": [{"name": tag} for tag in inputs["new_tags"]] if inputs["new_tags"] else []
    }
    
    # Prepare headers with credentials (assuming 'credential' contains a token or auth info)
    headers = {
        "Content-Type": "application/json"
    }
    
    # If credential is a dict, assume it has a 'token' key; if string, use as Bearer token directly
    if isinstance(inputs["credential"], dict):
        token = inputs["credential"].get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    elif isinstance(inputs["credential"], str) and inputs["credential"]:
        headers["Authorization"] = f"Bearer {inputs['credential']}"
    
    # Endpoint for updating a pet by ID
    url = f"{base_url}/pet/{inputs['new_resource_id']}"
    
    try:
        response = requests.put(url, json=payload, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Return the ID from the response if present, otherwise None
        return response.json().get("id") if response.json() else None
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")