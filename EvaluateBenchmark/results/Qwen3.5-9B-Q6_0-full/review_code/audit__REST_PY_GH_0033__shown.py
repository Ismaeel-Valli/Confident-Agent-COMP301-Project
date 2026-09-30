import requests

def solve(inputs):
    """
    Fetch a milestone from GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str)
            - repository_name (str)
            - milestone_number (int)
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response. None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    milestone_number = inputs["milestone_number"]
    credential = inputs["credential"]
    
    url = "https://api.github.com/repos/{owner}/{repo}/milestones/{number}".format(
        owner=owner,
        repo=repo,
        number=milestone_number
    )
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()