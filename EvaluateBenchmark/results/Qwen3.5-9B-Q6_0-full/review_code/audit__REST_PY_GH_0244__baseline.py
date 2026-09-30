import requests

def solve(inputs):
    """
    Updates a repository's 'delete_branch_on_merge' setting via the GitHub REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - "repository_owner" (str): The account owner of the repository.
            - "repository_name" (str): The name of the repository.
            - "new_delete_branch_on_merge" (bool or str): The new value for deleteBranchOnMerge.
            - "credential" (dict): Contains 'token' and optionally 'base_url'.
    
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty success response.
    
    Raises:
        Exception: If the HTTP response indicates failure (status code >= 400).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    delete_branch_on_merge = inputs["new_delete_branch_on_merge"]
    credential = inputs["credential"]

    # Construct the base URL if not provided in credentials
    base_url = credential.get("base_url", "https://api.github.com")
    
    # Prepare headers with Bearer token authentication
    headers = {
        "Authorization": f"Bearer {credential['token']}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    # Construct the URL for updating repository settings
    url = f"{base_url}/repos/{owner}/{repo}"

    # Prepare the payload
    payload = {
        "delete_branch_on_merge": delete_branch_on_merge
    }

    try:
        response = requests.put(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        
        # Return decoded JSON if present, otherwise None
        return response.json() if response.content else None

    except requests.exceptions.HTTPError as e:
        raise Exception(f"GitHub API request failed with status {response.status_code}: {e}")