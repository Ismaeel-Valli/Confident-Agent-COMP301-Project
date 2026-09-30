def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Dictionary containing:
            - new_category (str): Value for the category attribute
            - new_name (str): Value for the name attribute
            - new_photo_links (list or str): Value for the photoUrls attribute
            - new_tags (list): Value for the tags attribute
            - credential (str): Caller-supplied credential
    
    Returns:
        int or None: The response's id value, or None if absent. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    # Swagger Petstore base URL - OpenAPI declares /api/v3 as relative server
    base_url = "https://petstore3.swagger.io/api/v3"
    
    # Build the pet object from inputs
    pet = {
        "name": inputs["new_name"],
        "category": {"name": inputs["new_category"]},
        "photoUrls": inputs["new_photo_links"] if isinstance(inputs["new_photo_links"], list) else [inputs["new_photo_links"]],
        "tags": [{"name": tag} for tag in inputs["new_tags"]] if isinstance(inputs["new_tags"], list) else [{"name": inputs["new_tags"]}]
    }
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    # POST to /pet endpoint
    response = requests.post(f"{base_url}/pet", json=pet, headers=headers)
    
    # Check for unsuccessful HTTP response
    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to add pet: HTTP {response.status_code} - {response.text}")
    
    # Return the id from response, or None if absent
    data = response.json()
    return data.get("id")