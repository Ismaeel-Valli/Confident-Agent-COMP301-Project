import requests

def solve(inputs):
    """
    List branches for a GitHub repository using the REST API version 2026-03-10.
    
    Parameters:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git extension)
            - page (int): Page number of results to fetch
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response as a list of branches, or None if empty.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    # GitHub API v2026-03-10 endpoint for listing branches
    url = f"https://api.github.com/repos/{owner}/{repo}/branches"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {"page": page}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch branches: HTTP {response.status_code}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data