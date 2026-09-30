import requests
import json

def solve(inputs):
    """
    Create a label on a GitHub repository using the GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - new_description (str): Value for the description attribute
            - new_name (str): Value for the name attribute
            - credential (dict): Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    description = inputs["new_description"]
    name = inputs["new_name"]
    credential = inputs["credential"]
    
    # GitHub API v2026-03-10 endpoint for creating a label
    url = "https://api.github.com/repos/{owner}/{repo}/labels"
    url = url.format(owner=owner, repo=repo)
    
    headers = {
        "Authorization": f"token {credential.get('token', '')}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    data = {
        "name": name,
        "color": "FF0000",  # Default red color for new label
        "description": description
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        return response.json()
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to create label. Status code: {response.status_code}, Response: {response.text}")