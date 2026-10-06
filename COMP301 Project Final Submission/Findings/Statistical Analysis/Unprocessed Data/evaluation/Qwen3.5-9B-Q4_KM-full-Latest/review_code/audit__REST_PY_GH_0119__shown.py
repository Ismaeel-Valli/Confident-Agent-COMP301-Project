import requests
import json

def solve(inputs):
    """
    Create a milestone on a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner: str, account owner of the repository
            - repository_name: str, name of the repository (without .git)
            - new_description: str, value for description attribute
            - new_title: str, value for title attribute
            - credential: str, caller-supplied authentication token
    
    Returns:
        None if successful (empty response), otherwise decoded JSON response.
    
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    base_url = "https://api.github.com"
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    description = inputs["new_description"]
    title = inputs["new_title"]
    auth_token = inputs["credential"]
    
    url = f"{base_url}/repos/{owner}/{repo}/milestones"
    headers = {
        "Authorization": f"token {auth_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    payload = {
        "title": title,
        "description": description
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code not in (201, 202):
        response.raise_for_status()
    
    return response.json()