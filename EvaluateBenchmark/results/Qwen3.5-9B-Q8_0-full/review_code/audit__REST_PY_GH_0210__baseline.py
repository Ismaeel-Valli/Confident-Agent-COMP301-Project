import requests

def solve(inputs):
    """
    Lists pull requests for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - page_size (int): Number of results per page (max 100).
            - credential (str): Bearer token for authentication.
    
    Returns:
        list or None: Decoded JSON response as a list of pull requests, or None if empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page_size = min(inputs["page_size"], 100)
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {"per_page": page_size}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch pull requests. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    return None if len(data) == 0 else data