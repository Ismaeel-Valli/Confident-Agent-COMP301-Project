def solve(inputs):
    import requests
    
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    payload = {
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"]
    }
    
    response = requests.post(f"{base_url}{endpoint}", json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to add pet: {response.status_code} - {response.text}")
    
    return response.json().get("status")