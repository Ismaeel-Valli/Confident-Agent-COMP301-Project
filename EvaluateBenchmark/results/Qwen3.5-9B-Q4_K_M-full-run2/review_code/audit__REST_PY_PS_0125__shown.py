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
        "category": inputs["new_category"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "tags": inputs["new_tags"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        return response.json().get("name")
    elif response.status_code == 200:
        return response.json().get("name")
    else:
        raise Exception(f"Failed to add pet. Status code: {response.status_code}, Response: {response.text}")