import requests

def solve(inputs):
    """
    Fetches followers of a GitHub user using the GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'username' (str): The GitHub username.
            - 'page' (int): The page number of results to fetch.
            - 'credential' (str): The authentication token or Bearer token.
    
    Returns:
        list or None: A list of follower data dictionaries if followers exist, 
                      None if the response is successful but empty.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    username = inputs['username']
    page = inputs['page']
    credential = inputs['credential']
    
    url = f"https://api.github.com/users/{username}/followers?page={page}"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch followers. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    # GitHub returns an empty list [] when there are no followers on a page, 
    # which is a successful response but logically "empty".
    if not data:
        return None
    
    return data