import requests

def solve(inputs):
    """
    Update an existing pet in the Swagger Petstore API.
    
    Args:
        inputs (dict): Contains:
            - new_resource_id (int): The id value for the pet to update
            - new_name (str): The new name for the pet
            - new_photo_links (list): The new photo URLs for the pet
            - new_status (str): The new status for the pet
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response.
    
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
    
    response = requests.put(url, json=pet_data, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update pet: {response.status_code} - {response.text}")
    
    return response.json() if response.content else None