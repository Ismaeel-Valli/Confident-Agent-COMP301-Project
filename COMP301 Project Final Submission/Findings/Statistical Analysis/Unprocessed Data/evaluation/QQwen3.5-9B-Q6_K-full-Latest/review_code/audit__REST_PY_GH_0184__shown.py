import requests

def solve(inputs):
    """
    List milestones for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - page (int): Page number of results to fetch
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response, or None if successful but empty
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    # GitHub API v2026-03-10 endpoint for milestones
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones?page={page}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch milestones: HTTP {response.status_code}")
    
    data = response.json()
    
    # Return None for successful empty response
    if not data:
        return None
    
    return data