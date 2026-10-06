import requests

def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Must contain:
            - credential (str): API key or Bearer token for authentication.
            - new_name (str): Name of the new pet.
            - new_photo_links (list or str): Photo URLs for the pet.
            - new_status (str): Status of the new pet (e.g., 'available', 'pending', 'sold').
            - new_tags (list or str): Tags for the new pet.
    
    Returns:
        str or None: The name of the newly created pet, or None if absent.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://petstore3.swagger.io"
    url = f"{base_url}/api/v3/pet"  # Correct endpoint for adding a pet per OpenAPI spec
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"] if isinstance(inputs["new_photo_links"], list) else [inputs["new_photo_links"]],
        "status": inputs["new_status"],
        "tags": inputs["new_tags"] if isinstance(inputs["new_tags"], list) else [inputs["new_tags"]]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to add pet: {response.status_code} - {response.text}")
    
    return response.json().get("name")