import requests
import json

def solve(inputs):
    """
    List followers of a GitHub user.
    
    Args:
        inputs (dict): Contains 'username' and 'credential'.
        
    Returns:
        list or None: Decoded JSON response, or None for empty successful response.
        
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
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch followers: HTTP {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data