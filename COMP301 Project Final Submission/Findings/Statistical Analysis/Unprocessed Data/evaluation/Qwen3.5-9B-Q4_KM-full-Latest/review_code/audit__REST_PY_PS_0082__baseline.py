import requests

def solve(inputs):
    """
    Updates an existing pet in the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - new_category (str): Value for the category attribute.
            - new_resource_id (int): Value for the id attribute.
            - new_name (str): Value for the name attribute.
            - new_photo_links (list of str): Value for the photo URLs attribute.
            - new_tags (list of dict): Value for the tags attribute.
            - credential (dict): Caller-supplied credentials with necessary permissions.
    
    Returns:
        int or None: The response's status code, or None if the status is absent or the response is empty on success.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://petstore.swagger.io/v2"
    endpoint = "/pet"
    method = "PUT"
    
    # Prepare the payload for updating the pet
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "category": inputs["new_category"] if inputs["new_category"] else None,
        "photoUrls": inputs["new_photo_links"] if inputs["new_photo_links"] else None,
        "tags": inputs["new_tags"] if inputs["new_tags"] else None,
        "status": "available"  # Assuming we need to set a status; adjust if not required by the specific API version
    }
    
    # Prepare headers with credentials
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential'].get('token', '')}"  # Adjust based on actual credential structure
    }
    
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.request(method, url, json=payload, headers=headers)
        
        if response.status_code in [200, 204]:
            return None if response.text == "" else response.status_code
        
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")