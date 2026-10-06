import requests

def solve(inputs):
    """
    Lists repositories for a GitHub user based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'username' (str): The GitHub username.
            - 'type' (str, optional): Filter by repository type ('all', 'owner', or 'public').
            - 'sort' (str, optional): Property to sort results by ('created', 'updated', etc.).
            - 'credential' (dict): Contains authentication details (e.g., token).
    
    Returns:
        list or None: Decoded JSON response as a list of repositories. Returns None if the list is empty.
    
    Raises:
        Exception: If the HTTP response indicates an error.
    """
    username = inputs['username']
    repo_type = inputs.get('type', 'all')
    sort_by = inputs.get('sort', 'updated')
    credential = inputs['credential']

    # Construct the base URL for GitHub API v2026-03-10 (assuming standard endpoint structure)
    url = f"https://api.github.com/users/{username}/repos"

    # Build query parameters
    params = {}
    if repo_type != 'all':
        params['type'] = repo_type
    if sort_by:
        params['sort'] = sort_by

    # Prepare headers with authentication
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    # Extract token from credential (assumed structure: {'token': 'ghx_...'})
    auth_token = credential.get('token')
    if not auth_token:
        raise ValueError("Credential must contain a 'token' key.")

    headers["Authorization"] = f"Bearer {auth_token}"

    response = requests.get(url, params=params, headers=headers)

    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()

    data = response.json()

    # Return None if the response is an empty list
    return data if data else None