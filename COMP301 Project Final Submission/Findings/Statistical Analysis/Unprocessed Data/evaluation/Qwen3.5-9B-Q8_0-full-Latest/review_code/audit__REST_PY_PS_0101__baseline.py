import requests

def solve(inputs):
    """
    Adds a new pet to the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'credential': Authentication token or credentials.
            - 'new_resource_id': ID for the new pet.
            - 'new_name': Name for the new pet.
            - 'new_photo_links': List of photo URLs.
            - 'new_tags': List of tags.
    
    Returns:
        str or None: The ID of the created pet, or None if the response is empty/successful without an ID.
    
    Raises:
        requests.RequestException: If the HTTP request fails (non-2xx status).
    """
    base_url = "https://petstore.swagger.io/v2"
    url = f"{base_url}/pet"
    
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "tags": inputs["new_tags"],
        "status": "available"  # Default status as per OpenAPI spec
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise requests.RequestException(f"Failed to add pet. Status code: {response.status_code}, Response: {response.text}")
    
    # Try to extract 'id' from the JSON response
    try:
        data = response.json()
        return data.get("id")
    except ValueError:
        # If response is not JSON, treat as successful but no ID returned
        return None