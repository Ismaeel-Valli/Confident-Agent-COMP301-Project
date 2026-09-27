import requests

def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs: Dictionary containing:
            - new_category: str, value for the category attribute
            - new_name: str, value for the name attribute
            - new_photo_links: list of str, value for the photoUrls attribute
            - credential: str, caller-supplied credential (Bearer token)
    
    Returns:
        The decoded JSON response. For a successful empty response, returns None.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": inputs["new_name"],
        "category": {"name": inputs["new_category"]},
        "photoUrls": inputs["new_photo_links"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        return None
    elif response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to add pet. Status code: {response.status_code}, Response: {response.text}")