import requests

def solve(inputs):
    """
    Create a repository for the authenticated user via GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - "credential": str, Bearer token for authentication
            - "new_name": str, name for the new repository
            - "new_has_projects": bool, value for has_projects attribute
    
    Returns:
        None if successful (empty response), otherwise decoded JSON response.
    
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    payload = {
        "name": inputs["new_name"],
        "has_projects": inputs["new_has_projects"]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code not in (201, 202):
        response.raise_for_status()
        raise Exception(f"Failed to create repository: {response.text}")
    
    return None