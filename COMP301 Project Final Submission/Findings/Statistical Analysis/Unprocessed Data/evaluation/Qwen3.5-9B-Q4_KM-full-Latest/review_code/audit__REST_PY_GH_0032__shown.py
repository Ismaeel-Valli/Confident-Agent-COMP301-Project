import requests
import json

def solve(inputs):
    """
    Create a milestone on a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - new_title (str): Title for the milestone
            - credential (str): Bearer token for authentication
    
    Returns:
        None if successful (empty response), otherwise decoded JSON response.
    
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    title = inputs["new_title"]
    credential = inputs["credential"]
    
    url = "https://api.github.com/repos/{owner}/{repo}/milestones".format(
        owner=owner,
        repo=repo
    )
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    payload = {
        "title": title
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create milestone: {response.status_code} - {response.text}")
    
    return response.json()