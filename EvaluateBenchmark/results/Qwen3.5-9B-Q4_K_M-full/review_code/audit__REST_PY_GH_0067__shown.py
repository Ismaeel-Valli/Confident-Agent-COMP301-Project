import requests

def solve(inputs):
    """
    List organization repositories from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains 'organization', 'type', and 'credential'.
        
    Returns:
        list or None: Decoded JSON response, or None for empty successful response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    org = inputs["organization"]
    repo_types = inputs["type"]
    auth_token = inputs["credential"]
    
    url = "https://api.github.com/orgs/{org}/repos".format(org=org)
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {auth_token}"
    }
    
    params = {"type": repo_types}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data