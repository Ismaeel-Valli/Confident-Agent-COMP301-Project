import requests

def solve(inputs):
    """
    List repository issues from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - since (str): ISO 8601 timestamp for filtering issues updated after this time
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response, or None if successful but empty
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    since = inputs["since"]
    credential = inputs["credential"]
    
    # GitHub API v2026-03-10 endpoint for listing issues
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    params = {
        "since": since
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data