import requests
import json

def solve(inputs):
    """
    Update a GitHub organization using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - organization (str): The organization name
            - new_name (str): The new name for the organization
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    org = inputs["organization"]
    new_name = inputs["new_name"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for updating an organization
    url = f"https://api.github.com/orgs/{org}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Prepare the payload
    payload = {
        "name": new_name
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update organization: {response.status_code} - {response.text}")
    
    # Return decoded JSON response
    return response.json() if response.content else None