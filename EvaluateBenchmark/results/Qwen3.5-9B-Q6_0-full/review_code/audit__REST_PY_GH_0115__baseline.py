import requests

def solve(inputs):
    """
    Lists labels for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'page' (int): The page number of results to fetch.
            - 'credential' (str): The Bearer token for authentication.
    
    Returns:
        list or None: A list of label dictionaries if labels exist, otherwise None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx).
    """
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    page = inputs['page']
    credential = inputs['credential']
    
    url = f"https://api.github.com/repos/{owner}/{repo}/labels?page={page}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failed to fetch labels. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    # According to instructions: Return None for a successful empty response.
    if not data:
        return None
    
    return data