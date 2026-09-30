import requests
import json

def solve(inputs):
    """
    Update a GitHub organization using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - organization (str): The organization name to update.
            - new_name (str): The new name for the organization.
            - credential (str): Bearer token for authentication.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    org_name = inputs["organization"]
    new_name = inputs["new_name"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for updating an organization
    url = f"https://api.github.com/orgs/{org_name}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Prepare the payload for updating the organization name
    payload = {
        "name": new_name
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code == 204:
        # Successful update with empty response body
        return None
    elif response.status_code == 200:
        # Return the decoded JSON response
        return response.json()
    else:
        # Raise an exception for unsuccessful HTTP responses
        raise Exception(f"Failed to update organization: {response.status_code} - {response.text}")