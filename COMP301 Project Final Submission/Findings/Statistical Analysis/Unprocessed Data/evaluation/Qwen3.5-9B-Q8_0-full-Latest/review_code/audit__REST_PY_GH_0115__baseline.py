import requests

def solve(inputs):
    """
    Fetches labels for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - page (int): The page number of results to fetch.
            - credential (str): The caller-supplied credential (e.g., token).
    
    Returns:
        dict or None: Decoded JSON response if successful, or None for an empty list.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/labels?page={page}"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch labels: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response (empty list)
    if not data:
        return None
    
    return data