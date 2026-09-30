import requests

def solve(inputs):
    """
    Adds a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_name' (str): The name for the new pet.
            - 'new_photo_links' (list or str): Photo URLs for the new pet.
            - 'credential' (str): API key or token for authentication.
    
    Returns:
        str or None: The name of the newly created pet, or None if the response is empty/successful but lacks a name.
    
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    # Swagger Petstore OpenAPI 3 base URL (Public version)
    BASE_URL = "https://petstore3.swagger.io/api/v3/openapi.json"
    # We will use the actual add pet endpoint based on standard OpenAPI 3 structure for Petstore
    ADD_PET_URL = "https://petstore3.swagger.io/api/v3/pet"
    
    new_name = inputs.get('new_name')
    photo_links = inputs.get('new_photo_links', [])
    credential = inputs.get('credential')
    
    # Prepare the payload according to OpenAPI 3 Pet schema
    # id: optional, tag: optional, status: optional (default 'available'), category: optional
    pet_data = {
        "name": new_name,
        "photoUrls": photo_links if isinstance(photo_links, list) else [photo_links] if photo_links else [],
        "tags": [],
        "status": "available"
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": credential
    }
    
    try:
        response = requests.post(ADD_PET_URL, json=pet_data, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        
        # Check if the response contains a 'name' field
        if response.json():
            return response.json().get('name')
        else:
            return None
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Failed to add pet. HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")