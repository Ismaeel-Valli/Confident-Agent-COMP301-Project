import requests

def solve(inputs):
    """
    Create a label on a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git extension)
            - new_description (str): Value for the description attribute
            - new_name (str): Value for the name attribute
            - credential (str): Caller-supplied authentication token
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    description = inputs["new_description"]
    name = inputs["new_name"]
    credential = inputs["credential"]
    
    # GitHub API endpoint for creating a label
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    
    headers = {
        "Authorization": f"token {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    data = {
        "name": name,
        "color": "d73a4a",  # Default red color for labels
        "description": description
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        return response.json()
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to create label. Status code: {response.status_code}, Response: {response.text}")