import requests
import base64

def solve(inputs):
    """
    Create an organization repository on GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - organization (str): The organization name
            - new_description (str): Description for the repository
            - new_name (str): Name for the repository
            - credential (str): Base64-encoded username:password string
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    org = inputs["organization"]
    repo_name = inputs["new_name"]
    description = inputs["new_description"]
    credential = inputs["credential"]
    
    # Decode the credential (assumed to be base64-encoded "username:password")
    try:
        decoded_credential = base64.b64decode(credential).decode('utf-8')
    except Exception as e:
        raise ValueError(f"Invalid credential encoding: {e}")
    
    # GitHub API endpoint for creating a repository in an organization
    url = f"https://api.github.com/orgs/{org}/repos"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Basic {decoded_credential}",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    data = {
        "name": repo_name,
        "description": description
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code not in [201, 202]:  # Created or Accepted
        response.raise_for_status()
    
    # GitHub typically returns an empty response body for successful repo creation
    # Return None for successful empty response as per requirements
    return None