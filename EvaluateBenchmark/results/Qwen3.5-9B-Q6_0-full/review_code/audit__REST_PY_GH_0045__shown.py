import requests
import base64

def solve(inputs):
    """
    Get a release from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - release_id (int): Unique identifier of the release
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    release_id = inputs["release_id"]
    credential = inputs["credential"]
    
    # GitHub API v3 endpoint for releases by ID
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/{release_id}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"GitHub API request failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (though releases typically have data)
    if not data:
        return None
    
    return data