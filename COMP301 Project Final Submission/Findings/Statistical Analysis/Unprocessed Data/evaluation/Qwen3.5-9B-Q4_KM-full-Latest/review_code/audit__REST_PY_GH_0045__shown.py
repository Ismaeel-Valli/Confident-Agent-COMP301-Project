import requests

def solve(inputs):
    """
    Get a GitHub release by ID using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - release_id (int): Unique identifier of the release
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    release_id = inputs["release_id"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/releases/{release_id}"
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch release: HTTP {response.status_code}")
    
    return response.json()