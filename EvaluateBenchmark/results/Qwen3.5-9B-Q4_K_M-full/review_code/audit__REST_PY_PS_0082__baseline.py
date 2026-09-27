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
        int or None: The response's status code, or None if the status is absent or the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    # Construct the pet object to update
    pet = {
        "id": inputs["new_resource_id"],
        "category": {"name": inputs["new_category"]},
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "tags": inputs["new_tags"],
        "status": "available"  # Assuming we keep status as 'available' unless specified otherwise
    }

    # Base URL for Swagger Petstore API (assuming standard public instance)
    base_url = "https://petstore3.swagger.io/api/v3"
    
    # Endpoint to update a pet by ID
    url = f"{base_url}/pet/{inputs['new_resource_id']}"
    
    # Prepare headers with credentials
    headers = {
        "Content-Type": "application/json",
        "Authorization": inputs["credential"].get("token", "")  # Adjust based on credential structure
    }

    try:
        response = requests.put(url, json=pet, headers=headers)
        
        if response.status_code >= 400:
            raise Exception(f"Failed to update pet. Status code: {response.status_code}, Response: {response.text}")
        
        # Return status code if present, otherwise None for empty response
        return response.status_code if response.status_code != 204 else None
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")