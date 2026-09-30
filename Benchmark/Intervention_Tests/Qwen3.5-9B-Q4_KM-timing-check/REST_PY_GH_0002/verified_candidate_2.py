import requests

def solve(inputs):
    """
    Update an organization on GitHub using the REST API.
    
    Args:
        inputs (dict): Contains:
            - organization (str): The organization name.
            - new_name (str): The new name for the organization.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.github.com"
    org_name = inputs["organization"]
    new_name = inputs["new_name"]
    credential = inputs["credential"]
    
    url = f"{base_url}/orgs/{org_name}"
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {"name": new_name}
    
    response = requests.patch(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()