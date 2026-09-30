import requests
import json

def solve(inputs):
    """
    List repository issues for GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git extension)
            - creator (str): User that created the issue
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    creator = inputs["creator"]
    credential = inputs["credential"]
    
    # GitHub REST API v2026-03-10 endpoint for listing issues
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "creator": creator
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve issues: HTTP {response.status_code}, body: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data