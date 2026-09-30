import requests

def solve(inputs):
    """
    Get a milestone from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - milestone_number (int): Milestone number to retrieve
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    milestone_number = inputs["milestone_number"]
    credential = inputs["credential"]
    
    # GitHub REST API v3 endpoint for milestones
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones/{milestone_number}"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    # Raise exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for successful empty response (204 No Content)
    if response.status_code == 204:
        return None
    
    return data