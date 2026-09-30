def solve(inputs):
    """Add a new pet to the Swagger Petstore using provided inputs."""
    import requests
    
    # Base URL for Swagger Petstore (OpenAPI 3) - use /api/v3 as per OpenAPI spec
    base_url = "https://petstore3.swagger.io/api"
    
    # Build the endpoint URL for adding a pet
    url = f"{base_url}/v3/pet"
    
    # Prepare the request payload from inputs
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"]
    }
    
    # Make POST request with provided credential (assumed to be in header or body)
    headers = {"Authorization": f"Bearer {inputs['credential']}", "Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    
    # Raise exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"Failed to add pet. Status code: {response.status_code}, Response: {response.text}")
    
    # Return the id from response if present, otherwise None
    try:
        data = response.json()
        return data.get("id")
    except (ValueError, TypeError):
        # If response is not JSON or empty, return None for successful empty response
        return None