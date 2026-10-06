import requests

def solve(inputs):
    """
    Create a repository for the authenticated user on GitHub.
    
    Args:
        inputs (dict): Dictionary containing:
            - new_name (str): Name for the new repository
            - new_private (bool): Whether the repository should be private
            - credential (str): Authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    url = "https://api.github.com/user/repos"
    
    headers = {
        "Authorization": f"token {inputs['credential']}",
        "Accept": "application/vnd.github+json"
    }
    
    data = {
        "name": inputs["new_name"],
        "private": inputs["new_private"]
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code != 201 and response.status_code != 202:
        response.raise_for_status()
    
    return None