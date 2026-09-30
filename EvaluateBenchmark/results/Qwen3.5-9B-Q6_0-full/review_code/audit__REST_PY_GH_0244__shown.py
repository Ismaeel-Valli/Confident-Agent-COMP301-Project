import requests

def solve(inputs):
    """
    Update a repository on GitHub using the REST API v2026-03-10.
    
    Parameters:
        inputs (dict): Must contain:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - new_delete_branch_on_merge (bool or str): Value for deleteBranchOnMerge attribute.
            - credential (str): Bearer token for authentication.
    
    Returns:
        dict or None: Decoded JSON response. Returns None on successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    delete_branch_on_merge = inputs["new_delete_branch_on_merge"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for updating repository settings
    url = "https://api.github.com/repos/{owner}/{repo}".format(owner=owner, repo=repo)
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Prepare the payload
    payload = {"delete_branch_on_merge": delete_branch_on_merge}
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code == 204:
        return None
    elif response.status_code >= 400:
        raise Exception(f"Failed to update repository: {response.status_code} - {response.text}")
    
    return response.json()