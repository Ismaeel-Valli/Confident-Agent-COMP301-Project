import requests

def solve(inputs):
    """
    Updates an existing pet in the Swagger Petstore (OpenAPI 3 service).
    
    Parameters:
        inputs (dict): A dictionary containing:
            - 'credential': Authentication token or header value.
            - 'new_category': New category name for the pet.
            - 'new_resource_id': ID of the pet to update.
            - 'new_name': New name for the pet.
            - 'new_photo_links': List of photo URLs for the pet.
            - 'new_tags': List of tag dictionaries (e.g., [{'name': 'dog'}, {'name': 'friendly'}]).
    
    Returns:
        int or None: The HTTP status code of the response, or None if successful with no body/status.
    
    Raises:
        Exception: If the HTTP response indicates an error (status >= 400).
    """
    base_url = "https://petstore.swagger.io/v2"
    url = f"{base_url}/pet/{inputs['new_resource_id']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": inputs['new_name'],
        "category": {"name": inputs['new_category']} if inputs['new_category'] else None,
        "photoUrls": inputs['new_photo_links'] if inputs['new_photo_links'] else [],
        "tags": inputs['new_tags'] if inputs['new_tags'] else []
    }
    
    # Remove None fields to keep payload clean (optional but good practice)
    payload = {k: v for k, v in payload.items() if v is not None}

    response = requests.put(url, json=payload, headers=headers)
    
    status = response.status_code
    
    if status >= 400:
        raise Exception(f"Failed to update pet. Status code: {status}, Response: {response.text}")
    
    # Return None for successful empty response (e.g., 204 No Content)
    if status == 204 or (status == 200 and not response.text):
        return None
    
    return status