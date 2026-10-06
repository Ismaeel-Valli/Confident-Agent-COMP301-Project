def solve(inputs):
    """Add a new pet to the Swagger Petstore (OpenAPI 3 service)."""
    import requests
    
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to add pet: {response.status_code} - {response.text}")
    
    return response.json() if response.text else None