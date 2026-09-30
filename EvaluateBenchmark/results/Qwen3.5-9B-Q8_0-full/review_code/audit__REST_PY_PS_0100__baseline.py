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
            - credential (dict): Caller-supplied credentials (assumed to have necessary permissions).
    
    Returns:
        int or None: The ID of the updated pet, or None if absent or response is empty.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status code.
    """
    base_url = "https://petstore.swagger.io/v2"
    url = f"{base_url}/pet/{inputs['new_resource_id']}"
    
    # Prepare the payload based on provided inputs
    payload = {
        "id": inputs['new_resource_id'],
        "name": inputs['new_name'],
        "photoUrls": inputs['new_photo_links'],
        "status": inputs['new_status'],
        "tags": [{"name": tag} for tag in inputs['new_tags']] if inputs['new_tags'] else []
    }
    
    # Prepare headers with credentials (assuming 'credential' contains an 'Authorization' token or similar)
    headers = {
        "Content-Type": "application/json"
    }
    
    # If credential is a string, treat it as a Bearer token; otherwise, use as-is if it has necessary keys
    if isinstance(inputs['credential'], str):
        headers["Authorization"] = f"Bearer {inputs['credential']}"
    elif isinstance(inputs['credential'], dict) and 'token' in inputs['credential']:
        headers["Authorization"] = f"Bearer {inputs['credential']['token']}"
    
    try:
        response = requests.put(url, json=payload, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Return the 'id' from the response JSON if present and not empty
        if response.status_code == 204:
            return None
        
        try:
            response_data = response.json()
            return response_data.get('id')
        except ValueError:
            # If response is not JSON, assume success but no ID to return
            return None
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"A request error occurred: {e}")