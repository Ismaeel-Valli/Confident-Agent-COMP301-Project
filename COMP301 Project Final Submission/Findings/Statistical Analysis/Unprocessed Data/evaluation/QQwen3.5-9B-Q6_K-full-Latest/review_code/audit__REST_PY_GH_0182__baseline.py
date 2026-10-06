import requests
from urllib.parse import quote

def solve(inputs):
    """
    Fetches issue comments from a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git extension).
            - issue_number (int): The number that identifies the issue.
            - since (str, optional): ISO 8601 timestamp to filter comments updated after this time.
            - page_size (int, optional): Number of results per page (max 100).
            - credential (str): Bearer token for authentication.
    
    Returns:
        list or None: Decoded JSON response as a list of comments, or None if the response is empty.
        Raises:
            Exception: If the HTTP response status code indicates an error.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    issue_number = inputs["issue_number"]
    since = inputs.get("since")
    page_size = inputs.get("page_size", 30)
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {}
    if since:
        params["since"] = since
    if page_size:
        params["per_page"] = min(page_size, 100)
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch issue comments. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    return None if not data else data