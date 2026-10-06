import requests

def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Contains:
            - credential (str): Bearer token for authentication
            - new_category (str): Category value for the pet
            - new_name (str): Name value for the pet
            - new_photo_links (list): List of photo URLs for the pet
            - new_tags (list): List of tags for the pet
    
    Returns:
        dict or None: Decoded JSON response, or None if successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://petstore3.swagger.io"
    url = f"{base_url}/api/v3/pet"  # Using the correct API v3 endpoint for adding a pet
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    pet_data = {
        "name": inputs['new_name'],
        "photoUrls": inputs['new_photo_links'],
        "tags": [{"name": tag} for tag in inputs['new_tags']],
        "status": "available"  # Default status
    }
    
    response = requests.post(url, json=pet_data, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to add pet: HTTP {response.status_code} - {response.text}")
    
    return response.json() if response.content else None