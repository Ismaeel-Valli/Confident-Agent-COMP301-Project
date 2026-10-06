import requests

def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Dictionary containing:
            - new_name (str): Value for the name attribute
            - new_photo_links (list or str): Value for the photoUrls attribute
            - new_tags (list): Value for the tags attribute
            - credential (str): Caller-supplied credential (assumed to have necessary permissions)
    
    Returns:
        int or None: The response's id value, or None if that attribute is absent.
                     Returns None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    # Build the pet object from inputs
    photo_links = inputs["new_photo_links"] if isinstance(inputs["new_photo_links"], list) else [inputs["new_photo_links"]]
    tags_list = inputs["new_tags"] if isinstance(inputs["new_tags"], list) else [inputs["new_tags"]]
    
    pet_data = {
        "name": inputs["new_name"],
        "photoUrls": photo_links,
        "tags": [{"name": tag} for tag in tags_list]
    }
    
    try:
        response = requests.post(url, json=pet_data, headers=headers)
        
        # Check for unsuccessful HTTP response
        if response.status_code not in [200, 201]:
            raise Exception(f"Failed to add pet. Status code: {response.status_code}, Response: {response.text}")
        
        # Return the id from the response if present
        response_data = response.json()
        return response_data.get("id")
    
    except requests.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")