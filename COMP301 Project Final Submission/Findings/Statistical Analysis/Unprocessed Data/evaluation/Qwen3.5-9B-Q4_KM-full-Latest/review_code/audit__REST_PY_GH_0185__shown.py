import requests

def solve(inputs):
    """
    Create a milestone on a GitHub repository using the REST API v2026-03-10.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - new_description (str): Description for the milestone
            - new_state (str): State for the milestone ('open' or 'closed')
            - new_title (str): Title for the milestone
            - credential (str): Bearer token for authentication
    
    Returns:
        dict: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    description = inputs["new_description"]
    state = inputs["new_state"]
    title = inputs["new_title"]
    credential = inputs["credential"]
    
    url = "https://api.github.com/repos/{owner}/{repo}/milestones".format(
        owner=owner, repo=repo
    )
    
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    payload = {
        "title": title,
        "description": description,
        "state": state,
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create milestone. Status code: {response.status_code}, Response: {response.text}")
    
    return response.json()