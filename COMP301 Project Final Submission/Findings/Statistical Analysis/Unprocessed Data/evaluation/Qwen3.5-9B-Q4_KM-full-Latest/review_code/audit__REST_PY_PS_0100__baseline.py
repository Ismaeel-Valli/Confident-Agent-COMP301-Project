import requests

def solve(inputs):
    """
    Updates an existing pet in the Swagger Petstore (OpenAPI 3) service.
    
    Args:
        inputs (dict): A dictionary containing:
            - new_resource_id (str): The new ID for the pet.
            - new_name (str): The new name for the pet.
            - new_photo_links (list of str): The new photo URLs for the pet.
            - new_status (str): The new status for the pet.
            - new_tags (list of dict): The new tags for the pet, each with 'id' and 'name'.
            - credential (dict): Caller-supplied credentials (e.g., API key or token).
    
    Returns:
        str or None: The response's 'id' value if present, otherwise None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code outside 2xx/3xx range).
    """
    base_url = "https://petstore.swagger.io/v2"
    url = f"{base_url}/pet/{inputs['new_resource_id']}"
    
    payload = {
        "id": inputs["new_resource_id"],
        "name": inputs["new_name"],
        "photoUrls": inputs["new_photo_links"],
        "status": inputs["new_status"],
        "tags": inputs["new_tags"]
    }
    
    headers = {}
    if "credential" in inputs:
        # Assuming credential might be an API key or token; adjust based on actual Swagger Petstore auth method.
        # For standard Swagger Petstore, it often uses basic auth or no auth for public endpoints, 
        # but since credentials are provided, we'll assume a header like 'Authorization' or 'X-API-Key'.
        if isinstance(inputs["credential"], dict):
            if "api_key" in inputs["credential"]:
                headers["X-API-Key"] = inputs["credential"]["api_key"]
            elif "token" in inputs["credential"]:
                headers["Authorization"] = f"Bearer {inputs['credential']['token']}"
        else:
            # Fallback if credential is a string (e.g., token)
            headers["Authorization"] = f"Bearer {inputs['credential']}"
    
    response = requests.put(url, json=payload, headers=headers)
    
    if 200 <= response.status_code < 300:
        data = response.json()
        return data.get("id") if data else None
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")