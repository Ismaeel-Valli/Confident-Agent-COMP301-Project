import requests

def solve(inputs):
    """
    List pull requests for a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Repository name without .git extension
            - state (str): 'open', 'closed', or 'all'
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response. Returns None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    state = inputs["state"]
    credential = inputs["credential"]
    
    base_url = "https://api.github.com"
    endpoint = f"/repos/{owner}/{repo}/pulls"
    url = f"{base_url}{endpoint}"
    
    params = {
        "state": state
    }
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data