import requests

def solve(inputs):
    """
    Creates a pull request on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - new_base (str): Value for the base attribute.
            - new_body (str): Value for the body attribute.
            - new_draft (bool): Value for the draft attribute.
            - new_head (str): Value for the head attribute.
            - new_title (str): Value for the title attribute.
            - credential (str): The caller-supplied credential (token).
    
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    new_base = inputs["new_base"]
    new_body = inputs["new_body"]
    new_draft = inputs["new_draft"]
    new_head = inputs["new_head"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/pulls"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    payload = {
        "title": new_title,
        "body": new_body,
        "head": new_head,
        "base": new_base,
        "draft": new_draft
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create pull request. Status code: {response.status_code}, Response: {response.text}")
    
    return None