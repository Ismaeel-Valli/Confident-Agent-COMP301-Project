import requests

def solve(inputs):
    """
    Fetches followers of a GitHub user using the GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'username' (str): The GitHub username.
            - 'page' (int): The page number of results to fetch.
            - 'credential' (str): The bearer token for authentication.
    
    Returns:
        list or None: A list of follower data dictionaries, or None if the response is empty.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    username = inputs['username']
    page = inputs['page']
    credential = inputs['credential']
    
    url = f"https://api.github.com/users/{username}/followers"
    params = {
        'per_page': 100,
        'page': page
    }
    
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {credential}'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch followers. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data