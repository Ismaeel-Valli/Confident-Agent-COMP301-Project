import requests
import json


def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Must contain:
            - 'credential': API key or bearer token for authentication
            - 'new_name': Name of the new pet
            - 'new_category': Category of the new pet
            - 'new_photo_links': List of photo URLs for the new pet
    
    Returns:
        dict or None: Decoded JSON response from the API. Returns None on successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses (non-2xx status codes).
    """
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    payload = {
        "name": inputs["new_name"],
        "category": {
            "name": inputs["new_category"]
        },
        "photoUrls": inputs["new_photo_links"]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code < 200 or response.status_code >= 300:
            raise Exception(f"Failed to add pet. HTTP {response.status_code}: {response.text}")
        
        return response.json() if response.content else None
    
    except requests.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")