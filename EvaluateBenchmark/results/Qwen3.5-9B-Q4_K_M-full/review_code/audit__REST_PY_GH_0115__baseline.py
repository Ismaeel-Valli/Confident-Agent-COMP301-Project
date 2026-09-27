import requests

def solve(inputs):
    """
    Lists labels for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'page' (int): The page number of results to fetch.
            - 'credential' (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    page = inputs['page']
    credential = inputs['credential']

    # Construct the API URL for listing labels
    url = f"https://api.github.com/repos/{owner}/{repo}/labels?page={page}"

    headers = {
        "Accept": "application/vnd.github+json"
    }

    # Add authentication header if provided (assuming credential contains 'token' or similar)
    if isinstance(credential, dict):
        token = credential.get('token') or credential.get('access_token')
        if token:
            headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, headers=headers)

    # Raise an exception for unsuccessful HTTP responses (non-2xx)
    response.raise_for_status()

    data = response.json()

    # Return None for a successful empty response
    if not data:
        return None

    return data