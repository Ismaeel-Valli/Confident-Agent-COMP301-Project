import requests


def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Dictionary containing:
            - credential (str): Bearer token for authentication.
            - new_resource_id (int): Value for the 'id' attribute.
            - new_name (str): Value for the 'name' attribute.
            - new_photo_links (list[str]): Value for the 'photoUrls' attribute.
            - new_status (str): Value for the 'status' attribute.
    
    Returns:
        dict or None: Decoded JSON response from the API. Returns None on successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    pet_data = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"]
    }
    
    response = requests.post(url, json=pet_data, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to add pet. HTTP {response.status_code}: {response.text}")
    
    return response.json() if response.content else None