import requests


def solve(inputs):
    """
    Update an existing pet in the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Must contain:
            - new_resource_id (int): The id value for the updated pet.
            - new_name (str): The name value for the updated pet.
            - new_photo_links (list of str): The photoUrls value for the updated pet.
            - credential (str): Bearer token for authentication.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://petstore3.swagger.io"
    endpoint = "/v3/pet"
    url = f"{base_url}{endpoint}"
    
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
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    if len(response.content) == 0:
        return None
    
    return response.json()