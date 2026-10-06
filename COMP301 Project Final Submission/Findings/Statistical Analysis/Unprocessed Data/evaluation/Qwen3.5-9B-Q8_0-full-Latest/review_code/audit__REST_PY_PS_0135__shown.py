import requests

def solve(inputs):
    """
    Add a new pet to the Swagger Petstore API.
    
    Args:
        inputs (dict): Dictionary containing:
            - credential (str): Bearer token for authentication
            - new_name (str): Name of the new pet
            - new_category (str): Category of the new pet
            - new_photo_links (list): List of photo URLs
            - new_status (str): Status of the new pet
    
    Returns:
        str or None: The 'status' field from the response, or None if absent.
                     Returns None for successful empty responses.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://petstore3.swagger.io"
    url = f"{base_url}/api/v3/pet"  # Using the documented /api/v3 server path
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    pet_data = {
        "name": inputs["new_name"],
        "category": {"name": inputs["new_category"]},
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"]
    }
    
    response = requests.post(url, json=pet_data, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to add pet: {response.status_code} - {response.text}")
    
    return response.json().get("status")