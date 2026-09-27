def solve(inputs):
    """Add a new pet to the Swagger Petstore (OpenAPI 3 service).
    
    Args:
        inputs: Dictionary with keys:
            - new_name: str, value for the name attribute
            - new_photo_links: list of str, value for the photoUrls attribute
            - new_status: str, value for the status attribute
            - credential: str, caller-supplied credential
    
    Returns:
        The response's status value if present, or None if absent.
        Returns None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    import requests
    
    base_url = "https://petstore3.swagger.io"
    endpoint = "/api/v3/pet"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to add pet: HTTP {response.status_code}, body={response.text}")
    
    return response.json().get("status")