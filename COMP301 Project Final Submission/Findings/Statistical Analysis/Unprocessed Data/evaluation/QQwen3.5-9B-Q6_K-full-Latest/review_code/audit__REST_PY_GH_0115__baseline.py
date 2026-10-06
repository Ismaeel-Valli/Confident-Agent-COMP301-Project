import requests

def solve(inputs):
    """
    Fetches labels for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - page (int): The page number of results to fetch.
            - credential (str): The bearer token for authentication.
    
    Returns:
        list or None: A list of label dictionaries if labels exist, or None if the response is empty.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code indicates an error.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/labels?page={page}"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Request failed with status code: {response.status_code}")
    
    data = response.json()
    
    return data if data else None