import requests

def solve(inputs):
    """
    Update a milestone on GitHub using the REST API.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - milestone_number (int): Milestone number to update
            - new_title (str): New title for the milestone
            - credential (dict): Contains 'token' key with GitHub PAT
    
    Returns:
        None if successful (empty response), otherwise decoded JSON response.
    
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    milestone_num = inputs["milestone_number"]
    title = inputs["new_title"]
    token = inputs["credential"]["token"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/milestones/{milestone_num}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    payload = {"title": title}
    
    response = requests.patch(url, json=payload, headers=headers)
    response.raise_for_status()
    
    if response.status_code == 204:
        return None
    
    return response.json()