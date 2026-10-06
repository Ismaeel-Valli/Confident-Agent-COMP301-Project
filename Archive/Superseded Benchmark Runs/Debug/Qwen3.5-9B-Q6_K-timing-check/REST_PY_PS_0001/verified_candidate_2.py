import requests

def solve(inputs):
    """
    Update an existing pet in the Swagger Petstore API.
    
    Args:
        inputs (dict): Contains:
            - new_resource_id (int): New ID for the pet
            - new_name (str): New name for the pet
            - new_photo_links (list): New photo URLs for the pet
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet/{pet_id}"
    url = f"{base_url}{endpoint}".format(pet_id=inputs["new_resource_id"])
    
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
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update pet: {response.status_code} - {response.text}")
    
    return response.json() if response.content else None