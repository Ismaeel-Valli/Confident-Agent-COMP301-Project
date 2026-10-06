import requests
import json

def solve(inputs):
    """
    Update a repository's homepage on GitHub using the REST API v2026-03-10.
    
    Parameters:
        inputs (dict): Must contain:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - new_homepage (str): The new homepage URL to set.
            - credential (str): Bearer token for authentication.
    
    Returns:
        dict or None: Decoded JSON response if non-empty; None on success with empty body.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    new_homepage = inputs["new_homepage"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    payload = {"homepage": new_homepage}
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if 200 <= response.status_code < 300:
        data = response.json()
        return data if data else None
    else:
        raise Exception(f"Failed to update repository homepage. Status code: {response.status_code}, Response: {response.text}")