import requests
import base64

def solve(inputs):
    """
    Fetches the list of files in a GitHub pull request.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository.
            - pull_number (int): The number of the pull request.
            - credential (str): The caller-supplied credential (username:token).
    
    Returns:
        list or None: A list of dictionaries representing the files in the PR,
                      or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_number = inputs["pull_number"]
    credential = inputs["credential"]
    
    # Construct the API URL for GitHub v2026-03-10
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    
    # Prepare headers with authentication
    username, token = credential.split(":", 1)
    auth_string = f"{username}:{token}"
    encoded_auth = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Make the request
    response = requests.get(url, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    if not response.ok:
        raise Exception(f"GitHub API request failed with status {response.status_code}: {response.text}")
    
    # Decode and return the JSON response
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data