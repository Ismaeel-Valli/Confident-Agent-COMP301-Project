import requests

def solve(inputs):
    """
    List forks for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git extension)
            - sort (str): Sort order for results
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
    sort_order = inputs["sort"]
    page_size = inputs["page_size"]
    page_num = inputs["page"]
    credential = inputs["credential"]
    
    base_url = "https://api.github.com"
    endpoint = f"/repos/{owner}/{repo}/forks"
    url = f"{base_url}{endpoint}"
    
    params = {
        "sort": sort_order,
        "per_page": page_size,
        "page": page_num
    }
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    json_response = response.json()
    
    if len(json_response) == 0:
        return None
    
    return json_response