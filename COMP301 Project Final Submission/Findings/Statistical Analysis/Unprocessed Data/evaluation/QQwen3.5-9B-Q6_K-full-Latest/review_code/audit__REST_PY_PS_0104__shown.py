import requests

def solve(inputs):
    """
    Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs (dict): Dictionary containing:
            - credential (str): Caller-supplied API key/credential.
            - new_resource_id (int): Value for the id attribute.
            - new_name (str): Value for the name attribute.
            - new_photo_links (list of str): Value for the photoUrls attribute.
            - new_tags (list of dict): Value for the tags attribute.
    
    Returns:
        str or None: The response's 'name' value, or None if absent or successful empty response.
    
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
        "tags": inputs["new_tags"]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 201 or response.status_code == 200:
            data = response.json()
            return data.get("name")
        else:
            raise Exception(f"Unexpected status code: {response.status_code}")
    except requests.exceptions.HTTPError as e:
        if response.status_code >= 400:
            raise Exception(f"Failed to add pet: {e}")
        raise