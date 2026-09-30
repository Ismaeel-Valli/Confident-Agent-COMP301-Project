import requests

def solve(inputs):
    """
    Update a repository's homepage on GitHub using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository.
            - repository_name (str): Name of the repository (without .git).
            - new_homepage (str): New value for the homepage attribute.
            - credential (str): Bearer token for authentication.
    
    Returns:
        None if successful (empty response), otherwise decoded JSON response.
    
    Raises:
        Exception: If the HTTP response indicates failure (non-2xx status).
    """
    repo_owner = inputs["repository_owner"]
    repo_name = inputs["repository_name"]
    new_homepage = inputs["new_homepage"]
    credential = inputs["credential"]
    
    base_url = "https://api.github.com"
    url = f"{base_url}/repos/{repo_owner}/{repo_name}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    payload = {"homepage": new_homepage}
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code == 204:
        return None
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status {response.status_code}: {response.text}")
    
    return response.json()