import requests
import json

def solve(inputs):
    """
    Create a pull request on GitHub using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner: str, account owner of the repository
            - repository_name: str, name of the repository (without .git)
            - new_base: str, value for the base attribute
            - new_draft: bool/str, value for the draft attribute
            - new_head: str, value for the head attribute
            - new_title: str, value for the title attribute
            - credential: str, caller-supplied credential (assumed to have permissions)
    
    Returns:
        dict or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.github.com"
    repo = f"{inputs['repository_owner']}/{inputs['repository_name']}"
    url = f"{base_url}/repos/{repo}/pulls"
    
    headers = {
        "Authorization": f"token {inputs['credential']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    payload = {
        "title": inputs["new_title"],
        "body": "",
        "head": inputs["new_head"],
        "base": inputs["new_base"],
        "draft": inputs["new_draft"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        return None
    elif response.status_code in (200, 422):
        return response.json()
    else:
        raise Exception(f"Failed to create pull request. Status code: {response.status_code}, Response: {response.text}")