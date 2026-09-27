def solve(inputs):
    import requests
    
    base_url = "https://petstore3.swagger.io"
    headers = {"Authorization": f"Bearer {inputs['credential']}"}
    
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"]
    }
    
    response = requests.post(f"{base_url}/api/v3/pet", json=payload, headers=headers)
    
    if response.status_code == 201:
        return response.json().get("id")
    elif response.status_code == 200:
        return response.json().get("id")
    else:
        raise Exception(f"Failed to add pet: {response.status_code} {response.text}")