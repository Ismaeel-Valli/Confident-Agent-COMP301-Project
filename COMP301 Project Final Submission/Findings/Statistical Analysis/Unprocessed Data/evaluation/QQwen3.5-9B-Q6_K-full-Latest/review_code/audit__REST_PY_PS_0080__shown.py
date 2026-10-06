import requests

def solve(inputs):
    """Add a new pet to the Swagger Petstore and return its name."""
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    
    # Build the payload from inputs
    payload = {
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(f"{base_url}{endpoint}", json=payload, headers=headers)
    
    if response.status_code not in [200, 201]:
        raise Exception(f"Failed to add pet: HTTP {response.status_code} - {response.text}")
    
    # Return the name from the response, or None if absent
    data = response.json()
    return data.get("name")