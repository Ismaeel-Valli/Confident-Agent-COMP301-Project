import requests
import json


def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Dictionary containing:
            - credential (str): Bearer token for authentication
            - new_name (str): Name of the new pet
            - new_category (str): Category of the new pet
            - new_photo_links (list): List of photo URLs for the new pet
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://petstore3.swagger.io/api/v3"
    endpoint = "/pet"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    pet_data = {
        "name": inputs["new_name"],
        "category": {
            "name": inputs["new_category"]
        },
        "photoUrls": inputs["new_photo_links"]
    }
    
    response = requests.post(url, json=pet_data, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to add pet. Status code: {response.status_code}, Response: {response.text}")
    
    return response.json() if response.content else None