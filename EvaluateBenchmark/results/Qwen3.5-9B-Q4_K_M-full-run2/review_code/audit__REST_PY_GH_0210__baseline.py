import requests

def solve(inputs):
    """
    Lists pull requests for a GitHub repository using the specified API version.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - page_size (int): Number of results per page (max 100).
            - credential (dict): Caller-supplied credentials (assumed to have necessary permissions).
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is successfully empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page_size = inputs["page_size"]
    credential = inputs["credential"]

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    params = {
        "per_page": page_size
    }

    # Prepare authentication based on credential type (example: token or basic auth)
    if "token" in credential:
        headers["Authorization"] = f"Bearer {credential['token']}"
    elif "username" in credential and "password" in credential:
        auth = requests.auth.HTTPBasicAuth(credential["username"], credential["password"])
        # Note: Basic auth is deprecated for GitHub API; prefer token or app auth.
        # For this example, we'll use the token if available, else basic auth as fallback.
        pass  # We'll stick to token-based auth as it's more common and secure.

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to list pull requests: HTTP {response.status_code}, body: {response.text}")

    data = response.json()

    # Return None for successful empty response
    if not data:
        return None

    return data