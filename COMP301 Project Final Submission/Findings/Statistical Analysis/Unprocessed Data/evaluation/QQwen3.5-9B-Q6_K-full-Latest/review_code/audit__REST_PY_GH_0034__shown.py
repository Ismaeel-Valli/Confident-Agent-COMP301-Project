import requests
import json

def solve(inputs):
    """
    Update a milestone on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - milestone_number (int): Milestone number to update
            - new_title (str): New title for the milestone
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    milestone_number = inputs["milestone_number"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]
    
    # GitHub REST API endpoint for updating a milestone (PATCH method)
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones/{milestone_number}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Update the milestone with new title using PATCH
    payload = {
        "title": new_title
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to update milestone: {response.status_code} - {response.text}")
    
    # Return decoded JSON response
    return response.json()