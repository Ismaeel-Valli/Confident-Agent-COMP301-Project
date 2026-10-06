import requests

def solve(inputs):
    """
    Lists labels for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'credential' (str or dict): Caller-supplied credential (e.g., token string or dict with 'token').
    
    Returns:
        list or None: Decoded JSON response as a list of labels, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    credential = inputs["credential"]

    # Construct GitHub API URL for listing labels
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    # Prepare authentication header based on credential type
    if isinstance(credential, str):
        # Assume it's a token
        headers["Authorization"] = f"Bearer {credential}"
    elif isinstance(credential, dict) and "token" in credential:
        headers["Authorization"] = f"Bearer {credential['token']}"
    else:
        raise ValueError("Credential must be a string token or a dict with 'token' key.")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve labels: HTTP {response.status_code} - {response.text}")

    data = response.json()

    # Return None for successful empty response
    if not data:
        return None

    return data