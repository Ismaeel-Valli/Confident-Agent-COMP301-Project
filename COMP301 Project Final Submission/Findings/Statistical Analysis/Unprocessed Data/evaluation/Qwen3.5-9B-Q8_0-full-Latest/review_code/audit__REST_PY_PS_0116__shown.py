import requests

def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Dictionary containing:
            - new_resource_id (int): Value for the id attribute
            - new_name (str): Value for the name attribute
            - new_photo_links (list): Value for the photoUrls attribute
            - new_status (str): Value for the status attribute
            - credential (str): Caller-supplied credential
    
    Returns:
        str or None: The response's name value, or None if absent.
                     Returns None for a successful empty response.
    
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
    
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to add pet: {response.status_code} - {response.text}")
    
    return response.json().get("name")