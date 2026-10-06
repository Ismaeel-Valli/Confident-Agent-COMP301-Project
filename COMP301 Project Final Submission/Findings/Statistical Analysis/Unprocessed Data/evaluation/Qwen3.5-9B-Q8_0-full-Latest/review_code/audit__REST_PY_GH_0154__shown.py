import requests
import json

def solve(inputs):
    """
    Create a milestone on a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - new_due_on (str): Value for the due_on attribute
            - new_title (str): Value for the title attribute
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    due_on = inputs["new_due_on"]
    title = inputs["new_title"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for creating a milestone
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    data = {
        "title": title,
        "due_on": due_on
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        # Successful creation, return decoded JSON or None for empty response
        data = response.json()
        return data if data else None
    elif response.status_code == 202:
        # Accepted (async), return decoded JSON
        return response.json()
    else:
        # Unsuccessful response
        raise Exception(f"Failed to create milestone. Status code: {response.status_code}, Response: {response.text}")