import requests
import json

def solve(inputs):
    """
    List milestones for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): The account owner of the repository
            - repository_name (str): The name of the repository without .git extension
            - credential (str): Caller-supplied authentication token
    
    Returns:
        list or None: Decoded JSON response as a list, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    credential = inputs["credential"]
    
    # GitHub API v2026-03-10 endpoint for listing milestones
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, headers=headers)
    
    # Raise exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if len(data) == 0:
        return None
    
    return data