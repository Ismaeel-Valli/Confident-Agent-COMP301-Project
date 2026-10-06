import requests

def solve(inputs):
    """
    List repositories for the authenticated user on GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain 'page' (int) and 'credential' (str).
        
    Returns:
        list or None: Decoded JSON response, or None if successful but empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    page = inputs["page"]
    credential = inputs["credential"]
    
    url = "https://api.github.com/user/repos"
    params = {"page": page}
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data