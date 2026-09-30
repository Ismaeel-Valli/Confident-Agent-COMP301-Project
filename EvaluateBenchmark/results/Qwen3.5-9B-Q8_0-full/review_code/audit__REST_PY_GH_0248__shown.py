import requests

def solve(inputs):
    """
    List repository issues from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - since (str): ISO 8601 timestamp for filtering issues updated after this time
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://api.github.com"
    version = "2026-03-10"
    
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    since = inputs["since"]
    credential = inputs["credential"]
    
    # Construct the URL with query parameters
    url = f"{base_url}/repos/{owner}/{repo}/issues?state=all&per_page=100"
    
    # Add 'since' parameter if provided
    params = {}
    if since:
        params["since"] = since
    
    headers = {
        "Accept": f"application/vnd.github.{version}-preview+json",
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data