import requests
import json

def solve(inputs):
    """
    Create a milestone on a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - new_title (str): Title for the milestone
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    title = inputs["new_title"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for creating a milestone
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Create milestone data - GitHub requires at least a title for milestones
    payload = {
        "title": title
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        # Successful creation, return decoded JSON or None if empty
        data = response.json()
        return data if data else None
    elif response.status_code == 204:
        # No content response (also successful)
        return None
    else:
        # Unsuccessful response - raise exception
        response.raise_for_status()