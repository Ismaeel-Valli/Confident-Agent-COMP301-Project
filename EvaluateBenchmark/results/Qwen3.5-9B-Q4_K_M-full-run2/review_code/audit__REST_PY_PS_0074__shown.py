def solve(inputs):
    """Add a new pet to the Swagger Petstore (OpenAPI 3 service)."""
    import requests
    
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"]
    }
    
    response = requests.post(
        f"{base_url}{endpoint}",
        headers=headers,
        json=payload
    )
    
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to add pet: HTTP {response.status_code}, body={response.text}")
    
    return None