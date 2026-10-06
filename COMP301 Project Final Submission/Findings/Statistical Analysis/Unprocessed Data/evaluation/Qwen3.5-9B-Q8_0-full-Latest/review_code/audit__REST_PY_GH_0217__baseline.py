import requests
from urllib.parse import quote_plus

def solve(inputs):
    """
    Lists repositories for a GitHub user based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'username' (str): The GitHub username.
            - 'type' (str, optional): Filter by repository type ('all', 'owner', or 'member').
            - 'sort' (str, optional): Property to sort results by ('created', 'updated', 'pushed', 'full_name').
            - 'credential' (dict): Contains authentication details (e.g., token).
    
    Returns:
        list or None: Decoded JSON response as a list of repositories. Returns None if the list is empty.
        Raises:
            Exception: If the HTTP response indicates an error.
    """
    username = inputs['username']
    repo_type = inputs.get('type', 'all')
    sort_by = inputs.get('sort', 'created')
    
    # Construct the API URL for GitHub REST API version 2026-03-10
    base_url = "https://api.github.com"
    url = f"{base_url}/users/{quote_plus(username)}/repos"
    
    params = {}
    if repo_type:
        params['type'] = repo_type
    if sort_by:
        params['sort'] = sort_by
    
    # Prepare headers with authentication
    auth_token = inputs['credential'].get('token') or inputs['credential'].get('access_token')
    if not auth_token:
        raise ValueError("No valid credential token found in inputs.")
    
    headers = {
        'Authorization': f'token {auth_token}',
        'Accept': 'application/vnd.github+json'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for an empty list as per requirement
    return data if data else None