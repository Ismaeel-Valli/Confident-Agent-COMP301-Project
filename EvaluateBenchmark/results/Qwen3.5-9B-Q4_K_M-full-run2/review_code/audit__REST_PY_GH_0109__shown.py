def solve(inputs):
    """
    List repository contributors for GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): The account owner of the repository
            - repository_name (str): The name of the repository without .git extension
            - page_size (int): Number of results per page (max 100)
            - credential (str): Caller-supplied authentication token
    
    Returns:
        list or None: Decoded JSON response as a list, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page_size = inputs["page_size"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {credential}"
    }
    
    params = {"per_page": page_size}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data