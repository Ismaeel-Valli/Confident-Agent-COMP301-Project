import requests
import json

def solve(inputs):
    """
    Updates a repository on GitHub using the REST API version 2026-03-10.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'new_delete_branch_on_merge' (bool or str): Value for the delete branch on merge attribute.
            - 'credential' (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty and successful.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status code.
    """
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    delete_branch_on_merge = inputs['new_delete_branch_on_merge']
    credential = inputs['credential']
    
    # Construct the URL for updating repository settings
    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    # Prepare headers with authentication
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f"Bearer {credential.get('token', '')}" if isinstance(credential, dict) else ""
    }
    
    # Prepare payload
    payload = {
        "delete_branch_on_merge": delete_branch_on_merge
    }
    
    # Make the PATCH request to update the repository
    response = requests.patch(url, headers=headers, json=payload)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Return decoded JSON response or None if successful and empty
    return response.json() if response.text else None