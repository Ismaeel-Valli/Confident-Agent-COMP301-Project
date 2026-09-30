import requests

def solve(inputs):
    """
    Fetches a specific commit from a GitHub repository using the REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'page' (int): The page number of results to fetch.
            - 'page_size' (int): Number of results per page (max 100).
            - 'ref' (str): The commit reference (e.g., branch name, tag, or SHA).
            - 'credential' (str): The authentication token/secret.
    
    Returns:
        dict or None: The decoded JSON response if successful. Returns None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    page = inputs['page']
    page_size = inputs['page_size']
    ref = inputs['ref']
    credential = inputs['credential']

    # GitHub API endpoint for getting a specific commit
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{ref}"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    # Note: For a single commit by ref, pagination parameters (page, page_size) are typically not used 
    # as the endpoint returns exactly one commit object. However, we include them if the user expects 
    # to pass them, though they will be ignored by the API for this specific path.
    
    response = requests.get(url, headers=headers, auth=("token", credential))

    if response.status_code != 200:
        raise Exception(f"Failed to fetch commit: {response.status_code} - {response.text}")

    data = response.json()
    
    # Return None for a successful empty response (though unlikely for this endpoint)
    if not data:
        return None
    
    return data