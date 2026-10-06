import requests
from urllib.parse import quote

def solve(inputs):
    """
    Lists commits for a GitHub repository filtered by author.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository.
            - 'author' (str): GitHub username or email address to filter by commit author.
            - 'credential' (dict): Caller-supplied credential with 'token' key.
    
    Returns:
        list or None: Decoded JSON response as a list of commits, or None if the list is empty.
    
    Raises:
        Exception: If the HTTP response status code indicates an error.
    """
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    author = inputs["author"]
    credential = inputs["credential"]
    token = credential.get("token")

    if not token:
        raise ValueError("Missing authentication token in credentials.")

    url = f"https://api.github.com/repos/{quote(repository_owner, safe='')}/{quote(repository_name, safe='')}/commits"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    params = {}
    if author:
        params["author"] = author

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")

    data = response.json()
    
    return data if data else None