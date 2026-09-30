def solve(inputs):
    """Add a new pet to the Swagger Petstore API and return the pet's name."""
    import requests
    
    # Base URL for Swagger Petstore (OpenAPI 3)
    base_url = "https://petstore3.swagger.io/api/v3/openapi.json"
    
    # Prepare the payload for adding a new pet
    payload = {
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "tags": inputs["new_tags"]
    }
    
    # Make POST request to add the pet using the correct endpoint from OpenAPI spec
    response = requests.post(
        "https://petstore3.swagger.io/api/v3/pet",
        json=payload,
        headers={"Authorization": f"Bearer {inputs['credential']}"}
    )
    
    # Raise exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"Failed to add pet: HTTP {response.status_code}")
    
    # Return the name from the response, or None if absent
    data = response.json()
    return data.get("name")