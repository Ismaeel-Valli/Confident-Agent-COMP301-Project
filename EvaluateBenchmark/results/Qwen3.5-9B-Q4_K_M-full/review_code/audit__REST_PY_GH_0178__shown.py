def solve(inputs):
    """
    List forks of a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without .git extension.
            - sort (str): The sort order for the results.
            - page_size (int): The number of results per page (max 100).
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    sort_order = inputs["sort"]
    page_size = inputs["page_size"]
    credential = inputs["credential"]
    
    base_url = "https://api.github.com"
    endpoint = f"/repos/{owner}/{repo}/forks"
    url = f"{base_url}{endpoint}"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {credential}"
    }
    
    params = {
        "sort": sort_order,
        "per_page": page_size
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to list forks: HTTP {response.status_code}, body={response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data