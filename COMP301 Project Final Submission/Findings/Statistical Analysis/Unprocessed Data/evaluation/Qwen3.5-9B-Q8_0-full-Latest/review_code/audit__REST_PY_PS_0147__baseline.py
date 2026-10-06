import requests

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
        str or None: The ID of the newly created pet, or None if the response is empty/successful without an ID.
    
    Raises:
        requests.RequestException: If the HTTP request fails (non-successful status code).
    """
    # Base URL for Swagger Petstore OpenAPI 3
    base_url = "https://petstore.swagger.io/v2"
    endpoint = f"{base_url}/pet"
    
    # Prepare the payload based on inputs
    payload = {
        "category": {"name": inputs["new_category"]},
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "tags": [{"name": tag} for tag in inputs["new_tags"]] if inputs["new_tags"] else [],
        "status": "available"  # Default status as per common practice
    }
    
    # Prepare headers with the provided credential (assumed to be a Bearer token)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Return the 'id' from the response if present, otherwise None
        return response.json().get("id")
    
    except requests.RequestException as e:
        raise e