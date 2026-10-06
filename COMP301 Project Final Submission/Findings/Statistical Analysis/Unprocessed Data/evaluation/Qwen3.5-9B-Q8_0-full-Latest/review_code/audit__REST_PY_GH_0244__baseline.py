import requests

def solve(inputs):
    """
    Updates a repository on GitHub to set the 'delete_branch_on_merge' attribute.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository.
            - new_delete_branch_on_merge (bool or None): The new value for delete_branch_on_merge.
            - credential (str): The authentication token (Bearer token).
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    delete_branch_on_merge = inputs["new_delete_branch_on_merge"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    payload = {}
    if delete_branch_on_merge is not None:
        payload["delete_branch_on_merge"] = delete_branch_on_merge
    
    response = requests.patch(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update repository: {response.status_code} - {response.text}")
    
    return response.json() if response.text else None