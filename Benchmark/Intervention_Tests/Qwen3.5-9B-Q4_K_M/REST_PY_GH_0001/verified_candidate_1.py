import requests
import json

def solve(inputs):
    """
    Get an organization from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - organization (str): The organization name.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    org_name = inputs["organization"]
    auth_token = inputs["credential"]
    
    url = "https://api.github.com/orgs/{org}".format(org=org_name)
    headers = {
        "Authorization": f"token {auth_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to fetch organization {org_name}: HTTP {response.status_code}")