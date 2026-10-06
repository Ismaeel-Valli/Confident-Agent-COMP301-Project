import requests
import json

def solve(inputs):
    """
    Create an organization repository on GitHub using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - organization (str): Organization name
            - new_description (str): Description for the repository
            - new_name (str): Name for the repository
            - credential (str): Bearer token for authentication
    
    Returns:
        None if successful (empty response), otherwise decoded JSON response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.github.com"
    org = inputs["organization"]
    repo_name = inputs["new_name"]
    description = inputs["new_description"]
    auth_token = inputs["credential"]
    
    url = f"{base_url}/orgs/{org}/repos"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    payload = {
        "name": repo_name,
        "description": description
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code not in [201, 202]:
        response.raise_for_status()
    
    return None