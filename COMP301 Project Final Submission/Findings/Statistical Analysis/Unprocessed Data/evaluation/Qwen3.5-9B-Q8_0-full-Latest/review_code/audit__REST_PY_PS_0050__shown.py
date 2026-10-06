import requests

def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Dictionary containing:
            - credential (str): Caller-supplied credential for authentication.
            - new_name (str): Value for the name attribute.
            - new_category (str): Value for the category attribute.
            - new_photo_links (list): Value for the photoUrls attribute.
    
    Returns:
        int or None: The ID of the newly created pet, or None if absent.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    body = {
        "name": inputs["new_name"],
        "category": {"name": inputs["new_category"]},
        "photoUrls": inputs["new_photo_links"]
    }
    
    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to add pet: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data.get("id")