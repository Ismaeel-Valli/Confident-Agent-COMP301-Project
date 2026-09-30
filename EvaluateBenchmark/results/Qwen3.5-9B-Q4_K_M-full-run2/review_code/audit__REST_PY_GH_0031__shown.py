import requests
import json

def solve(inputs):
    """
    List milestones for a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - credential (str): Caller-supplied authentication token
    
    Returns:
        list or None: Decoded JSON response as a list, or None for empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones"
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data