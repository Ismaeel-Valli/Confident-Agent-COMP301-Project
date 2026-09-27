import requests
import json

def solve(inputs):
    """
    Lists labels for a GitHub repository using the REST API (version 2026-03-10).
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'credential' (str): Bearer token or OAuth token for authentication.
    
    Returns:
        dict or None: Decoded JSON response if labels exist, None if successful but empty.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status).
    """
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    token = inputs['credential']
    
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return None if len(data) == 0 else data
    elif response.status_code >= 400:
        raise Exception(f"GitHub API error {response.status_code}: {response.text}")
    
    raise Exception(f"Unexpected status code: {response.status_code}")