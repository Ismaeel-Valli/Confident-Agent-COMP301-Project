import requests

def solve(inputs):
    """
    Creates a new label in a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - new_color (str): Value for the color attribute of the label.
            - new_name (str): Value for the name attribute of the label.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        dict or None: The decoded JSON response if successful and non-empty, otherwise None.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    color = inputs["new_color"]
    name = inputs["new_name"]
    token = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/labels"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    data = {
        "name": name,
        "color": color
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create label. Status code: {response.status_code}, Response: {response.text}")
    
    return None