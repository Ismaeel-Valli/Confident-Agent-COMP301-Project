def solve(inputs):
    """
    Fetch an issue from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains repository_owner, repository_name, issue_number, and credential.
        
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    issue_number = inputs["issue_number"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return data if data else None
    elif response.status_code == 404:
        raise Exception(f"Resource not found: {url}")
    elif response.status_code == 403:
        raise Exception("Rate limit exceeded or insufficient permissions")
    else:
        raise Exception(f"HTTP error {response.status_code}: {response.text}")