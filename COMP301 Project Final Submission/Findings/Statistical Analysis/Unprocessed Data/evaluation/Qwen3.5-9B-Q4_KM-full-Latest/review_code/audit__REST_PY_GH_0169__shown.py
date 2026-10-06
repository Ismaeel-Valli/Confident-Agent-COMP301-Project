def solve(inputs):
    """
    List followers of a GitHub user using the GitHub REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains 'username', 'page_size' (max 100), 'page', and 'credential'.
        
    Returns:
        list or None: List of followers as decoded JSON, or None if empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    import requests
    
    username = inputs["username"]
    page_size = inputs["page_size"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    url = "https://api.github.com/users/{user}/followers".format(user=username)
    params = {
        "per_page": page_size,
        "page": page
    }
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data if len(data) > 0 else None