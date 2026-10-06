import requests

def solve(inputs):
    """
    Lists labels for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'credential' (str): The caller-supplied credential (e.g., token or Bearer token).
    
    Returns:
        list | None: A list of decoded JSON label objects, or None if the response is empty.
    
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    credential = inputs['credential']
    
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise requests.RequestException(f"Failed to fetch labels: {response.status_code} - {response.text}")
    
    data = response.json()
    
    return data if data else None