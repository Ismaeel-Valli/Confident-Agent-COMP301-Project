import requests
import json

def solve(inputs):
    """
    Create a repository for the authenticated user on GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - new_name (str): Name for the new repository
            - credential (str): Bearer token for authentication
    
    Returns:
        None if successful (empty response), otherwise decoded JSON response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    url = "https://api.github.com/user/repos"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/vnd.github+json"
    }
    
    payload = {
        "name": inputs["new_name"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        return None
    elif response.status_code == 422:
        # Repository already exists or other validation error
        return response.json()
    else:
        raise Exception(f"Failed to create repository. Status code: {response.status_code}, Response: {response.text}")