import requests

def solve(inputs):
    """
    Lists commits for a GitHub repository filtered by author.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git).
            - 'author' (str): GitHub username or email address to filter by commit author.
            - 'credential' (str): The caller-supplied credential (e.g., token) for authentication.
    
    Returns:
        dict or None: The decoded JSON response if commits are found, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    repository_owner = inputs['repository_owner']
    repository_name = inputs['repository_name']
    author = inputs['author']
    credential = inputs['credential']
    
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/commits"
    headers = {
        'Authorization': f'token {credential}',
        'Accept': 'application/vnd.github+json'
    }
    
    params = {
        'author': author
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failed to fetch commits. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data