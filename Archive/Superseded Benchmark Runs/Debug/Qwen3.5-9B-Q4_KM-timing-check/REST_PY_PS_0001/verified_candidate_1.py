import requests

def solve(inputs):
    """
    Update an existing pet in the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Contains:
            - new_resource_id (int): New value for the pet's id attribute.
            - new_name (str): New value for the pet's name attribute.
            - new_photo_links (list[str]): New value for the pet's photoUrls attribute.
            - credential (str): Caller-supplied Bearer token for authentication.
    
    Returns:
        dict or None: Decoded JSON response if successful; None for empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://petstore3.swagger.io"
    endpoint = "/v3/pet/{id}"
    url = base_url + endpoint.replace("{id}", str(inputs["new_resource_id"]))
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"]
    }
    
    response = requests.put(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    try:
        return response.json()
    except ValueError:
        raise Exception(f"Failed to decode JSON response: {response.text}")