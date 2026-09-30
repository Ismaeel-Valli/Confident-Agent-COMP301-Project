import requests

def solve(inputs):
    """
    Updates an existing pet in the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'credential': Authentication token or header value.
            - 'new_category': New category for the pet.
            - 'new_resource_id': ID of the pet to update.
            - 'new_name': New name for the pet.
            - 'new_photo_links': List of photo URLs.
            - 'new_tags': List of tags (each tag is a dict with 'name' and optional 'id').
    
    Returns:
        int or None: The status code of the response, or None if the response body is empty on success.
    
    Raises:
        Exception: If the HTTP response indicates an error.
    """
    base_url = "https://petstore.swagger.io/v2"
    pet_id = inputs['new_resource_id']
    credential = inputs['credential']
    
    # Prepare the payload for updating the pet
    payload = {
        "name": inputs['new_name'],
        "category": {"id": None, "name": inputs['new_category']},
        "photoUrls": inputs['new_photo_links'],
        "tags": inputs['new_tags'],
        "status": "available"  # Assuming status needs to be set; adjust if not required
    }

    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }

    url = f"{base_url}/pet/{pet_id}"

    try:
        response = requests.put(url, json=payload, headers=headers)
        
        if response.status_code >= 400:
            raise Exception(f"Failed to update pet. Status code: {response.status_code}, Response: {response.text}")
        
        # Return status code unless the response is empty (204 No Content)
        if response.status_code == 204 or not response.text.strip():
            return None
        
        return response.status_code

    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")