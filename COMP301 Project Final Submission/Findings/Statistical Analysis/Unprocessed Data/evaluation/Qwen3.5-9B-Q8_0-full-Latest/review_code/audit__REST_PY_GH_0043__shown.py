import requests
import json

def solve(inputs):
    """
    Create a release on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - new_tag_name (str): Value for the tag name attribute
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    tag_name = inputs["new_tag_name"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for creating a release
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Required fields for creating a release
    data = {
        "tag_name": tag_name,
        "name": tag_name,  # Release name defaults to tag name if not specified
        "draft": False,     # Non-draft release
        "prerelease": False # Not a prerelease
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 201:  # 201 Created is expected for new releases
        response.raise_for_status()
    
    # Return decoded JSON response
    return response.json()