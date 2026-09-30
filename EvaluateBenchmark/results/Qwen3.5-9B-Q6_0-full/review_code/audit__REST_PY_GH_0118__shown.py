import requests
import json


def solve(inputs):
    """
    List milestones for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str): The account owner of the repository
            - repository_name (str): The name of the repository (without .git)
            - sort (str): What to sort results by
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response, or None if successful but empty
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    sort_by = inputs["sort"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {
        "sort": sort_by
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch milestones: HTTP {response.status_code}")
    
    data = response.json()
    
    return data if len(data) > 0 else None