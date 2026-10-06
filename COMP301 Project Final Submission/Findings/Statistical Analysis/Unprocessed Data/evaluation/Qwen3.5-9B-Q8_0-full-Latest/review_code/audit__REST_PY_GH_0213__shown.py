import requests
import json

def solve(inputs):
    """
    Create a release on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - new_prerelease (bool): Value for prerelease attribute
            - new_tag_name (str): Value for tag name attribute
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    prerelease = inputs["new_prerelease"]
    tag_name = inputs["new_tag_name"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for creating a release
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    data = {
        "tag_name": tag_name,
        "name": tag_name,  # Using tag_name as name since not specified
        "prerelease": prerelease
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 201 and response.status_code != 200:
        raise Exception(f"Failed to create release. Status code: {response.status_code}, Response: {response.text}")
    
    # Return decoded JSON response
    if response.content:
        return response.json()
    else:
        return None