import requests

def solve(inputs):
    """
    Lists the people a GitHub user follows using the GitHub REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'username' (str): The handle for the GitHub user account.
            - 'page' (int): The page number of the results to fetch.
            - 'credential' (str): The credential string (e.g., Bearer token) for authentication.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, 
                      None if the response is successfully empty.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    username = inputs['username']
    page = inputs['page']
    credential = inputs['credential']
    
    # Construct the API URL for following users
    url = f"https://api.github.com/users/{username}/following"
    
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {credential}'
    }
    
    params = {
        'page': page,
        'per_page': 100  # GitHub default max per page is usually 30, but we can request up to 100
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch following users: HTTP {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data