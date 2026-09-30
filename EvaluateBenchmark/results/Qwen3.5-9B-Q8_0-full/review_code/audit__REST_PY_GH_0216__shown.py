import requests


def solve(inputs):
    """
    Create a repository for the authenticated user via GitHub REST API v2026-03-10.
    
    Parameters:
        inputs (dict): Must contain:
            - 'credential': str, token or auth header value
            - 'new_name': str, name of the new repository
            - 'new_has_projects': bool, whether the repo should have projects enabled
    
    Returns:
        dict or None: Decoded JSON response. Returns None on successful empty response.
    
    Raises:
        Exception: On unsuccessful HTTP response (non-2xx).
    """
    base_url = "https://api.github.com"
    headers = {
        "Authorization": f"token {inputs['credential']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    url = f"{base_url}/user/repos"
    payload = {
        "name": inputs["new_name"],
        "has_projects": inputs["new_has_projects"]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"GitHub API request failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    
    # GitHub returns empty body for successful repo creation in some cases, but typically returns the created repo object.
    # The spec says return None for a successful empty response.
    if not data:
        return None
    
    return data