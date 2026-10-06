import requests

def solve(inputs):
    """
    Updates a repository on GitHub using the REST API version 2026-03-10.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'new_delete_branch_on_merge' (bool or str): Value for the delete_branch_on_merge attribute.
            - 'credential' (str): Bearer token or OAuth token for authentication.
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty success response.
    
    Raises:
        Exception: If the HTTP response indicates failure (status code >= 400).
    """
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    delete_branch_on_merge = inputs['new_delete_branch_on_merge']
    credential = inputs['credential']

    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    payload = {
        "delete_branch_on_merge": delete_branch_on_merge
    }

    response = requests.put(url, json=payload, headers=headers)

    if response.status_code >= 400:
        raise Exception(f"Failed to update repository: {response.status_code} - {response.text}")

    return response.json() if response.text else None