def solve(inputs):
    """
    Update a pull request on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - pull_number (int): Pull request number
            - new_body (str): New body content for the pull request
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    import requests
    
    # Construct the API URL
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_number = inputs["pull_number"]
    new_body = inputs["new_body"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    payload = {
        "body": new_body
    }
    
    response = requests.patch(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update pull request: {response.status_code} - {response.text}")
    
    return response.json() if response.content else None