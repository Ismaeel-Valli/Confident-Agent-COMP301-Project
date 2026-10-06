import requests

def solve(inputs):
    """
    Updates a pull request on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - pull_number (int): The number identifying the pull request.
            - new_state (str): The new state for the pull request.
            - new_title (str): The new title for the pull request.
            - credential (dict): Caller-supplied credentials containing 'token'.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    pull_number = inputs["pull_number"]
    new_state = inputs["new_state"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/pulls/{pull_number}"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
        "Authorization": f"Bearer {credential['token']}"
    }
    
    payload = {
        "state": new_state,
        "title": new_title
    }
    
    response = requests.put(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update pull request. Status code: {response.status_code}, Response: {response.text}")
    
    return None