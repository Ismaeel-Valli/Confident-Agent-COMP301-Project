import requests

def solve(inputs):
    """
    Lists commits for a GitHub repository filtered by author.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - author (str): GitHub username or email address to filter by commit author.
            - credential (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
        list|None: Decoded JSON response as a list, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    author = inputs["author"]
    credential = inputs["credential"]
    
    # Construct the API URL for listing commits with author filter
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    
    # Prepare headers using the provided credential (assumed to contain 'token' or similar)
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential.get('token', '')}"
    }
    
    params = {"author": author}
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Return None for a successful empty response
    return data if data else None