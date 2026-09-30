import requests
import json

def solve(inputs):
    """
    Get organization details from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain 'organization' and 'credential'.
        
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    org_name = inputs["organization"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/orgs/{org_name}"
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v2026-03-10+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch organization: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data if data else None