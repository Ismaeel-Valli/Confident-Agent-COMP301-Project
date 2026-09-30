def solve(inputs):
    import requests
    
    pet_id = inputs["pet_identifier"]
    status = inputs["status"]
    credential = inputs["credential"]
    
    url = "https://petstore3.swagger.io/api/v3/pet"
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    payload = {
        "name": pet_id,
        "status": status,
        "photoUrls": []
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update pet: {response.text}")
    
    data = response.json()
    
    if "name" in data:
        return data["name"]
    elif response.status_code == 204 or (isinstance(data, dict) and len(data) == 0):
        return None
    
    return None