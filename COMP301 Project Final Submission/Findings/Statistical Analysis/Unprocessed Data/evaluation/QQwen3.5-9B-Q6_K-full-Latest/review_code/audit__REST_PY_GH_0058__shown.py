import requests

def solve(inputs):
    """
    Check if a GitHub repository is starred by the authenticated user.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): The account owner of the repository
            - repository_name (str): The name of the repository without .git extension
            - credential (str): Bearer token for authentication
    
    Returns:
        int: Successful HTTP status code (204 for not starred, 200 for starred)
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/user/starred/{owner}/{repo}"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 204:
        return 204
    elif response.status_code == 200:
        return 200
    else:
        raise Exception(f"Failed to check star status: {response.status_code}")