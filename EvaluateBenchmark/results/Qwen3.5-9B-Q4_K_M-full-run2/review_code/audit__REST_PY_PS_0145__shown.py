def solve(inputs):
    """Add a new pet to the Swagger Petstore (OpenAPI 3 service)."""
    import requests
    
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "category": {"name": inputs["new_category"]},
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "tags": [{"name": tag} for tag in inputs["new_tags"]] if isinstance(inputs["new_tags"], list) else [{"name": inputs["new_tags"]}]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to add pet: HTTP {response.status_code}, body={response.text}")
    
    return response.json() if response.content else None