import requests

def solve(inputs):
    """
    Create a repository for the authenticated user on GitHub.
    
    Args:
        inputs (dict): Contains:
            - new_name (str): Name of the new repository.
            - new_has_wiki (bool): Whether to enable wiki for the repository.
            - credential (str): Bearer token for authentication.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.github.com"
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    url = f"{base_url}/user/repos"
    params = {
        "name": inputs["new_name"],
        "has_wiki": inputs["new_has_wiki"]
    }
    
    response = requests.post(url, headers=headers, json=params)
    
    if response.status_code not in (201, 202):
        response.raise_for_status()
    
    return response.json() if response.text else None