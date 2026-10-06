import requests
from requests.exceptions import RequestException, HTTPError

def solve(inputs):
    """
    Updates a repository on GitHub by setting the 'delete_branch_on_merge' attribute.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git extension).
            - new_delete_branch_on_merge (bool or str): The value for delete_branch_on_merge.
            - credential (dict): Contains 'token' key with the GitHub personal access token.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        Exception: If the HTTP request is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    delete_branch_on_merge = inputs["new_delete_branch_on_merge"]
    token = inputs["credential"]["token"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    payload = {
        "delete_branch_on_merge": delete_branch_on_merge
    }
    
    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 204:
            return None
        
        return response.json()
    
    except HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except RequestException as req_err:
        raise Exception(f"Request error occurred: {req_err}")