import requests

def solve(inputs):
    """
    Lists the people a GitHub user follows using the GitHub REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'username' (str): The GitHub username.
            - 'credential' (str): The bearer token for authentication.
    
    Returns:
        list or None: A list of usernames followed by the user, or None if empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    username = inputs['username']
    credential = inputs['credential']
    
    url = f"https://api.github.com/users/{username}/following"
    headers = {
        'Authorization': f'Bearer {credential}',
        'Accept': 'application/vnd.github+json'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch following list. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    # GitHub API returns a list of user objects under the 'following' endpoint
    if not data:
        return None
    
    return [user['login'] for user in data]