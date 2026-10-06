import requests
import json
from urllib.parse import quote

def solve(inputs):
    """
    Create an organization repository on GitHub using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - organization (str): The organization name
            - new_has_issues (bool): Value for the has_issues attribute
            - new_name (str): Value for the repository name
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    """
    org = inputs["organization"]
    repo_name = inputs["new_name"]
    has_issues = inputs["new_has_issues"]
    credential = inputs["credential"]
    
    # GitHub API v2026-03-10 endpoint for creating a repository in an organization
    base_url = "https://api.github.com"
    url = f"{base_url}/orgs/{quote(org)}/repos"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    payload = {
        "name": repo_name,
        "has_issues": has_issues
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    # Raise exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"Failed to create repository: {response.status_code} - {response.text}")
    
    # Return decoded JSON response
    data = response.json()
    
    # Return None for successful empty response (though GitHub typically returns repo object)
    if not data:
        return None
    
    return data