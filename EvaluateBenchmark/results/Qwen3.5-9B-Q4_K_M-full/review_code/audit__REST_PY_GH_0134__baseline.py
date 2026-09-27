import requests

def solve(inputs):
    """
    Lists followers of a GitHub user using the GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'username' (str): The handle for the GitHub user account.
            - 'page' (int): The page number of the results to fetch.
            - 'credential' (str): The Bearer token or OAuth token for authentication.
    
    Returns:
        dict or None: The decoded JSON response if followers are found, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response status code indicates an error (non-2xx).
    """
    username = inputs['username']
    page = inputs['page']
    credential = inputs['credential']
    
    url = f"https://api.github.com/users/{username}/followers"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "page": page,
        "per_page": 100  # GitHub default max per page is 100
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch followers for {username}: HTTP {response.status_code}, Body: {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response (empty list of followers)
    if not data:
        return None
    
    return data