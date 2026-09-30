import requests

def solve(inputs):
    """
    Update an existing pet in Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Contains:
            - new_resource_id (int): The id value for the pet to update.
            - new_name (str): The new name for the pet.
            - new_photo_links (list of str): The new photo URLs for the pet.
            - credential (str): The Bearer token for authentication.
    
    Returns:
        str or None: The name value from the response, or None if absent or empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code >= 400).
    """
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    url = f"{base_url}{endpoint}"
    
    pet_data = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"]
    }
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    response = requests.put(url, json=pet_data, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update pet: {response.status_code} - {response.text}")
    
    try:
        data = response.json()
        return data.get("name")
    except (ValueError, TypeError):
        return None