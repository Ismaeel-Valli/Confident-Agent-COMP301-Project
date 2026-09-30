def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Contains:
            - credential (str): Bearer token for authentication
            - new_name (str): Name of the pet
            - new_category (str): Category of the pet
            - new_photo_links (list): List of photo URLs
            - new_status (str): Status of the pet
    
    Returns:
        int or None: The ID of the created pet, or None if response is empty.
    
    Raises:
        Exception: If HTTP response indicates failure.
    """
    import requests
    
    # Base URL for Swagger Petstore API
    base_url = "https://petstore3.swagger.io/api/v3/openapi.json"
    
    # Prepare the pet object according to OpenAPI 3 specification
    pet_data = {
        "name": inputs["new_name"],
        "category": {"name": inputs["new_category"]},
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"]
    }
    
    # Make POST request to add the pet
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(
        "https://petstore3.swagger.io/api/v3/pet",
        json=pet_data,
        headers=headers
    )
    
    # Check for successful response
    if response.status_code >= 400:
        raise Exception(f"Failed to add pet: {response.status_code} - {response.text}")
    
    # Return the ID from response or None if absent
    result = response.json()
    return result.get("id")