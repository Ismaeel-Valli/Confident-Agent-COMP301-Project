import requests

def solve(inputs):
    """
    List followers of a GitHub user.
    
    Args:
        inputs (dict): Contains 'username', 'page_size', 'page', and 'credential'.
        
    Returns:
        list or None: Decoded JSON response, or None for empty successful response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    username = inputs["username"]
    page_size = inputs["page_size"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    # GitHub API v3 endpoint for user followers
    url = f"https://api.github.com/users/{username}/followers"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {credential}"
    }
    
    params = {
        "per_page": page_size,
        "page": page
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch followers. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response
    if not data:
        return None
    
    return data