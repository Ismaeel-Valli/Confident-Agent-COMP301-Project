import requests

def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Dictionary containing:
            - new_category (str): Value for the category attribute
            - new_resource_id (int): Value for the id attribute
            - new_name (str): Value for the name attribute
            - new_photo_links (list): Value for the photoUrls attribute
            - credential (str): Caller-supplied credential (assumed to have necessary permissions)
    
    Returns:
        int or None: The response's status value, or None if that attribute is absent.
                     Returns None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    url = f"{base_url}{endpoint}"
    
    # Prepare the pet data payload
    pet_data = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "category": {"name": inputs["new_category"]},
        "photoUrls": inputs["new_photo_links"],
        "tags": [],
        "status": "available"
    }
    
    # Prepare headers with the credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=pet_data, headers=headers)
        
        # Check if the response is successful (2xx status code)
        if 200 <= response.status_code < 300:
            # Return None for a successful empty response or if 'status' attribute is absent
            if "status" in response.json():
                return response.json()["status"]
            else:
                return None
        else:
            # Raise an exception for an unsuccessful HTTP response
            raise Exception(f"Failed to add pet. Status code: {response.status_code}, Response: {response.text}")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")