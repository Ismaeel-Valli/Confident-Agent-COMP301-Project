import requests
import json

def solve(inputs):
    """
    Get an organization from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain 'organization' and 'credential'.
        
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    org = inputs["organization"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/orgs/{org}"
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    elif response.status_code in (401, 403):
        raise Exception(f"Authentication failed: {response.status_code}")
    else:
        raise Exception(f"Failed to fetch organization: {response.status_code} - {response.text}")