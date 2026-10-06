import requests

def solve(inputs):
    """
    List repositories for a GitHub user.
    
    Args:
        inputs (dict): Dictionary containing:
            - username (str): The handle for the GitHub user account.
            - type (str, optional): Limit results to repositories of the specified type.
            - sort (str, optional): The property to sort the results by.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        list or None: Decoded JSON response as a list of repositories, or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    username = inputs["username"]
    repo_type = inputs.get("type")
    sort_by = inputs.get("sort")
    credential = inputs["credential"]
    
    base_url = "https://api.github.com"
    url = f"{base_url}/users/{username}/repos"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {}
    if repo_type:
        params["type"] = repo_type
    if sort_by:
        params["sort"] = sort_by
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for successful empty response (empty list)
    if not data:
        return None
    
    return data