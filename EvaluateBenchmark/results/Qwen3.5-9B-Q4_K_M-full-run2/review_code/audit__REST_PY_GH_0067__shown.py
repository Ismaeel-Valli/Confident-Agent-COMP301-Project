import requests

def solve(inputs):
    """
    List organization repositories for GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - organization (str): The organization name
            - type (list): Types of repositories to return
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    org = inputs["organization"]
    repo_types = inputs["type"]
    auth_token = inputs["credential"]
    
    # Build query parameters for repository types
    params = {"per_page": 30}
    if repo_types:
        params["sort"] = "created"
        params["direction"] = "asc"
    
    url = f"https://api.github.com/orgs/{org}/repos"
    headers = {
        "Authorization": f"token {auth_token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data