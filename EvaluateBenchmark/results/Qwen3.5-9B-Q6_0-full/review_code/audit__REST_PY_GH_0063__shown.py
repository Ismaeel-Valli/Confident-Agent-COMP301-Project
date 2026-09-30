import requests
import base64

def solve(inputs):
    """
    List the people a GitHub user follows using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Must contain 'username' and 'credential'.
        
    Returns:
        list or None: Decoded JSON response, or None if empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    username = inputs["username"]
    credential = inputs["credential"]
    
    # GitHub API v3 endpoint for following users
    url = f"https://api.github.com/users/{username}/following"
    
    # Prepare headers with authentication
    auth_string = base64.b64encode(credential.encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_string}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch following users: HTTP {response.status_code}")
    
    data = response.json()
    
    # If empty list, return None as per requirement
    if not data:
        return None
    
    return data