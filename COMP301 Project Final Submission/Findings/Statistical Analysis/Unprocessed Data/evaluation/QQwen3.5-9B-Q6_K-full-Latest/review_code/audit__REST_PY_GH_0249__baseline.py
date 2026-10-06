import requests

def solve(inputs):
    """
    Creates an issue in a GitHub repository using the GitHub REST API.
    
    Parameters:
    inputs (dict): A dictionary containing the following keys:
        - 'repository_owner': str, the account owner of the repository
        - 'repository_name': str, the name of the repository without the .git extension
        - 'new_assignees': list or None, value for the assignees attribute
        - 'new_body': str, value for the body attribute
        - 'new_labels': list or None, value for the labels attribute
        - 'new_title': str, value for the title attribute
        - 'credential': dict, containing 'token' key with the GitHub token
    
    Returns:
    dict or None: The decoded JSON response. Returns None for a successful empty response.
    
    Raises:
    Exception: For an unsuccessful HTTP response.
    """
    
    repository_owner = inputs['repository_owner']
    repository_name = inputs['repository_name']
    new_assignees = inputs['new_assignees']
    new_body = inputs['new_body']
    new_labels = inputs['new_labels']
    new_title = inputs['new_title']
    credential = inputs['credential']
    
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/issues"
    
    headers = {
        'Authorization': f'token {credential["token"]}',
        'Accept': 'application/vnd.github+json'
    }
    
    data = {
        'title': new_title,
        'body': new_body
    }
    
    if new_assignees is not None:
        data['assignees'] = new_assignees
    
    if new_labels is not None:
        data['labels'] = new_labels
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 201:
        response.raise_for_status()
    
    return response.json()