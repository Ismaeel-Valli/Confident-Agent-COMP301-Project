import requests

def solve(inputs):
    """
    Updates a pull request on GitHub using the REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - pull_number (int): The number that identifies the pull request.
            - new_body (str): The new value for the body attribute.
            - new_title (str): The new value for the title attribute.
            - credential (dict): Caller-supplied credentials (e.g., token in 'token' key).
    
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
    
    Raises:
        Exception: If the HTTP response indicates failure (status code >= 400).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_number = inputs["pull_number"]
    new_body = inputs["new_body"]
    new_title = inputs["new_title"]
    credential = inputs["credential"]

    # Construct the API URL for GitHub REST API (version 2026-03-10 is hypothetical; 
    # we use the standard format which remains consistent across versions)
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    # Prepare the payload for updating the pull request
    payload = {
        "title": new_title,
        "body": new_body
    }

    # Include authentication header if a token is provided in the credential dict
    if "token" in credential:
        headers["Authorization"] = f"Bearer {credential['token']}"

    response = requests.put(url, json=payload, headers=headers)

    # Raise an exception for unsuccessful HTTP responses (status code >= 400)
    if response.status_code >= 400:
        raise Exception(f"Failed to update pull request. Status code: {response.status_code}, Response: {response.text}")

    # Return the decoded JSON response, or None if the response is empty
    return response.json() if response.content else None