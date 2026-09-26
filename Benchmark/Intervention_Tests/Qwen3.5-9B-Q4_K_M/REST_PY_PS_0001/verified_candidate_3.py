import requests

def solve(inputs):
    base_url = "https://petstore3.swagger.io"
    new_resource_id = inputs["new_resource_id"]
    new_name = inputs["new_name"]
    new_photo_links = inputs["new_photo_links"]
    credential = inputs["credential"]
    
    url = f"{base_url}/api/v3/pet/{new_resource_id}"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    payload = {
        "id": new_resource_id,
        "name": new_name,
        "photoUrls": new_photo_links
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    try:
        return response.json()
    except Exception:
        raise Exception("Failed to decode JSON response")