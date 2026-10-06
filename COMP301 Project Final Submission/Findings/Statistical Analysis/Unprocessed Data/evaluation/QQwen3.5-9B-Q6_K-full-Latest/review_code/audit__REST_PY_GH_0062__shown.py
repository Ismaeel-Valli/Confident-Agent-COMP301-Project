import requests

def solve(inputs):
    """
    List followers of a GitHub user using the GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain 'username' and 'credential'.
        
    Returns:
        list or None: Decoded JSON response, or None if empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    username = inputs["username"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/users/{username}/followers"
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
    
    return data