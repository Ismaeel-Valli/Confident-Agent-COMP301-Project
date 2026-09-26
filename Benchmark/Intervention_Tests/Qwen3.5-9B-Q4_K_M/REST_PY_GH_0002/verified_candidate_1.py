import requests

def solve(inputs):
    """
    Update an organization on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - organization (str): The organization name to update.
            - new_name (str): The new name for the organization.
            - credential (str): Bearer token for authentication.
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response indicates an error.
    """
    base_url = "https://api.github.com"
    version = "2026-03-10"
    org_name = inputs["organization"]
    new_name = inputs["new_name"]
    credential = inputs["credential"]
    
    url = f"{base_url}/orgs/{org_name}"
    headers = {
        "Accept": f"application/vnd.github.{version}",
        "Authorization": f"Bearer {credential}"
    }
    
    payload = {"name": new_name}
    
    response = requests.put(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()