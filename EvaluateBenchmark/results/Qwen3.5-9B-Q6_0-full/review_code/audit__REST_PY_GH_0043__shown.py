import requests
import json


def solve(inputs):
    """
    Create a release on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str): The account owner of the repository
            - repository_name (str): The name of the repository without .git extension
            - new_tag_name (str): Value for the tag name attribute
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    tag_name = inputs["new_tag_name"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    data = {
        "tag_name": tag_name,
        "name": tag_name,
        "draft": False,
        "prerelease": False
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create release. Status code: {response.status_code}, Response: {response.text}")
    
    return response.json()