import requests

def solve(inputs):
    """
    Lists labels for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'credential' (str): The caller-supplied credential (e.g., Bearer token or API key).
    
    Returns:
        dict or None: The decoded JSON response if labels exist, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    credential = inputs['credential']
    
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch labels for {owner}/{repo}. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    # GitHub returns an empty list [] when there are no labels.
    # The instructions say to return None for a successful empty response.
    if len(data) == 0:
        return None
    
    return data