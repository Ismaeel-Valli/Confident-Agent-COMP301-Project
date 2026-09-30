import requests

def solve(inputs):
    """
    Update a pull request on GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - pull_number (int): Pull request number
            - new_body (str): New body content for the PR
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_number = inputs["pull_number"]
    new_body = inputs["new_body"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    payload = {
        "body": new_body
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()