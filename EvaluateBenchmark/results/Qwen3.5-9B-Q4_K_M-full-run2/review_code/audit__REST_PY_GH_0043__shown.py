import requests
import json

def solve(inputs):
    """
    Create a release on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - new_tag_name (str): Tag name for the release
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    tag = inputs["new_tag_name"]
    token = inputs["credential"]
    
    url = "https://api.github.com/repos/{owner}/{repo}/releases"
    url = url.format(owner=owner, repo=repo)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    payload = {
        "tag_name": tag,
        "name": tag,
        "draft": False,
        "prerelease": False
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code not in [201, 202]:
        response.raise_for_status()
    
    return response.json() if response.text else None