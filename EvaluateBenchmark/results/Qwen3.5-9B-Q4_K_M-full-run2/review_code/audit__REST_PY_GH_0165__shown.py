import requests

def solve(inputs):
    """
    List watchers for a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - page_size (int): Number of results per page (max 100)
            - page (int): Page number to fetch
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page_size = inputs["page_size"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    base_url = "https://api.github.com"
    endpoint = f"/repos/{owner}/{repo}/subscribers"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "per_page": page_size,
        "page": page
    }
    
    response = requests.get(base_url + endpoint, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch watchers: HTTP {response.status_code}")
    
    data = response.json()
    
    return data if data else None