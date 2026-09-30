def solve(inputs):
    import requests
    
    pet_id = inputs["pet_identifier"]
    status = inputs["status"]
    credential = inputs["credential"]
    
    url = "https://petstore3.swagger.io/api/v3/pet"
    headers = {"Authorization": f"Bearer {credential}"}
    payload = {"name": "", "photoUrls": [], "id": pet_id, "status": status}
    
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    data = response.json()
    if "id" in data:
        return data["id"]
    return None