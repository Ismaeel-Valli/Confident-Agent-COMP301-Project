import requests

def solve(inputs):
    """
    List watchers for a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - page (int): Page number of results to fetch
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/subscribers"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {credential}"
    }
    
    params = {"page": page}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data if data else None