import requests

def solve(inputs):
    """
    Updates an existing pet in the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - new_resource_id (str): The new ID for the pet.
            - new_name (str): The new name for the pet.
            - new_photo_links (list of str): The new photo URLs for the pet.
            - credential (str): The caller-supplied credential (e.g., API key or token).
    
    Returns:
        int or None: The status code of the response, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status.
    """
    base_url = "https://petstore.swagger.io/v2"
    url = f"{base_url}/pet/{inputs['new_resource_id']}"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential']}" if inputs['credential'].startswith("Bearer ") else inputs['credential']
    }
    
    payload = {
        "id": inputs['new_resource_id'],
        "name": inputs['new_name'],
        "photoUrls": inputs['new_photo_links']
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update pet. Status code: {response.status_code}, Response: {response.text}")
    
    return None if response.text.strip() == "" else response.status_code