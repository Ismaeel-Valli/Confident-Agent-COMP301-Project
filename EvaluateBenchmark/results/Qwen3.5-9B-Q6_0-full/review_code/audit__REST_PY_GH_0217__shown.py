import requests
import json


def solve(inputs):
    """
    List repositories for a GitHub user.
    
    Args:
        inputs (dict): Contains 'username', 'type', 'sort', and 'credential'.
        
    Returns:
        list or None: Decoded JSON response, or None if empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    username = inputs["username"]
    repo_type = inputs.get("type")
    sort_by = inputs.get("sort")
    credential = inputs["credential"]
    
    base_url = "https://api.github.com"
    url = f"{base_url}/users/{username}/repos"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    params = {}
    if repo_type:
        params["type"] = repo_type
    if sort_by:
        params["sort"] = sort_by
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data