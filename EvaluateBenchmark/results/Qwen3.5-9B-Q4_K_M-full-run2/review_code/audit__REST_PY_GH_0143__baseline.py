import requests

def solve(inputs):
    """
    Fetches a specific commit from a GitHub repository using the REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - page (int): Page number for pagination (not applicable for single commit, but included per spec).
            - page_size (int): Number of results per page (max 100, not applicable for single commit, but included per spec).
            - ref (str): The commit reference (e.g., branch name, tag, or SHA).
            - credential (dict): Caller-supplied credentials (assumed to have necessary permissions).
    
    Returns:
        dict or None: Decoded JSON response if successful. Returns None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    ref = inputs["ref"]
    credential = inputs["credential"]
    
    # Construct the API URL for fetching a commit by SHA or ref
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{ref}"
    
    headers = {
        "Accept": "application/vnd.github+json"
    }
    
    # Add authentication if provided (assuming credential contains 'token' key for Bearer auth)
    if isinstance(credential, dict) and "token" in credential:
        headers["Authorization"] = f"Bearer {credential['token']}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # GitHub returns an empty list for some edge cases or null, but typically a commit object.
        # If the response is logically empty (e.g., list with no items), return None.
        if isinstance(data, list) and len(data) == 0:
            return None
        return data
    else:
        raise Exception(f"Failed to fetch commit: HTTP {response.status_code}, Response: {response.text}")