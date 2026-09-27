def solve(inputs):
    """Add a new pet to the Swagger Petstore (OpenAPI 3 service)."""
    import requests
    
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    response = requests.post(f"{base_url}{endpoint}", json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to add pet: HTTP {response.status_code}")
    
    try:
        data = response.json()
        return data.get("name")
    except (ValueError, TypeError):
        return None