import requests

def solve(inputs):
    """
    List repository contributors from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git extension)
            - page_size (int): Number of results per page (max 100)
            - credential (str): Caller-supplied authentication token
    
    Returns:
        list or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page_size = inputs["page_size"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for contributors
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    
    # Prepare headers with Bearer token authentication
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    # Make the API request
    response = requests.get(url, headers=headers)
    
    # Raise exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"GitHub API request failed with status {response.status_code}: {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response, otherwise return the list
    if len(data) == 0:
        return None
    
    return data