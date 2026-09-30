import requests

def solve(inputs):
    """
    List forks of a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
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
    
    url = f"https://api.github.com/repos/{owner}/{repo}/forks"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "per_page": page_size
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch forks: HTTP {response.status_code}")
    
    data = response.json()
    
    # Return None for successful empty response
    if len(data) == 0:
        return None
    
    return data