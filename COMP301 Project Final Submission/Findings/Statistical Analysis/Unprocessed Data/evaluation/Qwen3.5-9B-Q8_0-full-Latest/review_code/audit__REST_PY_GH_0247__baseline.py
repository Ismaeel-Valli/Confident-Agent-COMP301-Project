import requests

def solve(inputs):
    """
    Fetches forks for a given GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - sort (str): The sort order for the results.
            - page_size (int): Number of results per page (max 100).
            - page (int): Page number to fetch.
            - credential (str): Bearer token for authentication.
    
    Returns:
        list or None: Decoded JSON response as a list, or None if the list is empty.
        Raises:
            requests.RequestException: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    sort_order = inputs["sort"]
    page_size = inputs["page_size"]
    page_number = inputs["page"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/forks"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {
        "sort": sort_order,
        "per_page": page_size,
        "page": page_number
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if not response.ok:
        raise requests.RequestException(f"Failed to fetch forks: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return None if len(data) == 0 else data