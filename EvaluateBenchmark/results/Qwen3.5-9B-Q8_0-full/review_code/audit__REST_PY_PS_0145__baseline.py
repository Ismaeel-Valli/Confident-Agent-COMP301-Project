import requests
import json

def solve(inputs):
    """
    Adds a new pet to the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'credential': Authentication token or credentials.
            - 'new_category': Category of the new pet.
            - 'new_resource_id': ID for the new pet.
            - 'new_name': Name of the new pet.
            - 'new_photo_links': List of photo URLs for the new pet.
            - 'new_tags': List of tags for the new pet.
    
    Returns:
        dict or None: Decoded JSON response if successful (empty), otherwise raises an exception.
    """
    base_url = "https://petstore.swagger.io/v2"
    url = f"{base_url}/pet"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    payload = {
        "id": inputs['new_resource_id'],
        "name": inputs['new_name'],
        "category": {"name": inputs['new_category']},
        "photoUrls": inputs['new_photo_links'],
        "tags": [{"name": tag} for tag in inputs['new_tags']],
        "status": "available"  # Default status as per OpenAPI spec
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200 or response.status_code == 201:
            if response.text.strip():
                return response.json()
            else:
                return None
        else:
            raise Exception(f"Failed to add pet. HTTP Status Code: {response.status_code}, Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error occurred: {str(e)}")