import requests

def solve(inputs):
    """
    Get a milestone from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - milestone_number (int): Milestone number to retrieve
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    milestone = inputs["milestone_number"]
    token = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones/{milestone}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve milestone: {response.status_code} - {response.text}")
    
    return response.json()