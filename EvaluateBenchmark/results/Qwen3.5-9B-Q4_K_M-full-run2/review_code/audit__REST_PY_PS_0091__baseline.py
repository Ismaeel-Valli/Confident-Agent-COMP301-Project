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
            - new_status (str): Value for the status attribute.
            - credential (dict): Caller-supplied credentials with necessary permissions.
    
    Returns:
        str or None: The response's 'name' value if present, otherwise None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://petstore.swagger.io/v2"
    pet_id = inputs["new_resource_id"]
    update_payload = {
        "id": pet_id,
        "category": inputs["new_category"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"]
    }

    # Prepare headers with credentials (assuming 'credential' contains an 'Authorization' token or similar)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {inputs['credential'].get('token', '')}" if isinstance(inputs['credential'], dict) else ""
    }

    url = f"{base_url}/pet/{pet_id}"
    response = requests.put(url, json=update_payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to update pet. Status code: {response.status_code}, Response: {response.text}")

    # Return the 'name' value from the response if present, otherwise None for an empty response
    return response.json().get("name") if response.json() else None