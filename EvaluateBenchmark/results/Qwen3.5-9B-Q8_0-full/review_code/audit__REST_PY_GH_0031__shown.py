import requests

def solve(inputs):
    """
    List milestones for a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - credential (str): Bearer token for authentication
    
    Returns:
        list or None: Decoded JSON response. Returns None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch milestones: HTTP {response.status_code}")
    
    data = response.json()
    
    # Return None for empty successful response
    return None if len(data) == 0 else data