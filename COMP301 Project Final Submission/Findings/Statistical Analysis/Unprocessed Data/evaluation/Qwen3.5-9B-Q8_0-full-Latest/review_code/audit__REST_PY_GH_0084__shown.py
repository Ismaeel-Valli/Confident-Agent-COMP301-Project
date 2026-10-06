import requests
import json

def solve(inputs):
    """
    Update a milestone on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - milestone_number (int): Milestone number to update
            - new_state (str): New state value for the milestone
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    milestone_number = inputs["milestone_number"]
    new_state = inputs["new_state"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for updating a milestone (v2026-03-10)
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones/{milestone_number}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Only the state field is required for updating a milestone
    payload = {
        "state": new_state
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update milestone: {response.status_code} - {response.text}")
    
    # GitHub returns an empty body for successful updates (200 OK)
    if response.status_code == 200 and len(response.content) == 0:
        return None
    
    return response.json()