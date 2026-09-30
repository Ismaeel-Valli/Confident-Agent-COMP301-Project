import requests

def solve(inputs):
    """
    Lists commits for a GitHub repository filtered by author.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'author' (str): GitHub username or email to filter by.
            - 'credential' (str): Bearer token for authentication.
    
    Returns:
        list or None: Decoded JSON response as a list of commits, or None if empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    author = inputs['author']
    credential = inputs['credential']
    
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {'author': author}
    headers = {
        'Authorization': f'Bearer {credential}',
        'Accept': 'application/vnd.github+json'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch commits. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    return data if data else None