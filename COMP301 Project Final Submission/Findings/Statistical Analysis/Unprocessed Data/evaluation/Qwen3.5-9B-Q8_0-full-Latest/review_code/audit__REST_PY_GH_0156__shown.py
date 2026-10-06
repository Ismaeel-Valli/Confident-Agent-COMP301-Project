import requests

def solve(inputs):
    """
    List pull requests for a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - base (str): Base branch name to filter pull requests
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response, or None if empty
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    base_branch = inputs["base"]
    credential = inputs["credential"]
    
    # GitHub API v2026-03-10 endpoint for listing pull requests
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?base={base_branch}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list)
    return data if data else None