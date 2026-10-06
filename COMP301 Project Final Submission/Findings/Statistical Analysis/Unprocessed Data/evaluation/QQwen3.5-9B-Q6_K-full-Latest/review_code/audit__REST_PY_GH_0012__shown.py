import requests

def solve(inputs):
    """
    Fetch a commit from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Repository name without .git extension
            - ref (str): Commit reference (branch, tag, or SHA)
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses (non-2xx status codes).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    ref = inputs["ref"]
    credential = inputs["credential"]
    
    # GitHub REST API v2026-03-10 endpoint for getting a commit
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{ref}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v2+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failed to fetch commit: HTTP {response.status_code}")
    
    data = response.json()
    
    # Return None for successful empty response (though commits are rarely empty)
    if not data:
        return None
    
    return data