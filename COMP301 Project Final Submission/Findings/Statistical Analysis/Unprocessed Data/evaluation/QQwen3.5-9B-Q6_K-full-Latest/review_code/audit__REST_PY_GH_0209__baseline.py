import requests
import json


def solve(inputs):
    """
    Updates a milestone in a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'milestone_number' (int): The milestone number to update.
            - 'new_description' (str): New description for the milestone.
            - 'new_title' (str): New title for the milestone.
            - 'credential' (dict): Caller-supplied credentials with 'token'.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    milestone_number = inputs['milestone_number']
    new_description = inputs['new_description']
    new_title = inputs['new_title']
    credential = inputs['credential']
    
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones/{milestone_number}"
    headers = {
        'Authorization': f'token {credential["token"]}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2026-03-10'
    }
    
    payload = {
        "title": new_title,
        "description": new_description
    }
    
    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update milestone. Status code: {response.status_code}, Response: {response.text}")
    
    return None