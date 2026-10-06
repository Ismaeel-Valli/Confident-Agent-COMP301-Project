import requests

def solve(inputs):
    """
    Update an issue on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without .git extension.
            - issue_number (int): The number that identifies the issue.
            - new_body (str): The new value for the body attribute.
            - credential (str): The caller-supplied authentication token.
    
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response indicates an unsuccessful status code.
    """
    # Construct the API URL for updating an issue (PATCH method)
    base_url = "https://api.github.com"
    version = "2026-03-10"
    
    # GitHub API v3 uses /repos/{owner}/{repo}/issues/{issue_number}
    url = f"{base_url}/repos/{inputs['repository_owner']}/{inputs['repository_name']}/issues/{inputs['issue_number']}"
    
    # Prepare the headers with authentication and the Accept header for JSON
    headers = {
        "Authorization": f"token {inputs['credential']}",
        "Accept": f"application/vnd.github.{version}-preview+json"
    }
    
    # Prepare the payload to update only the body field
    payload = {
        "body": inputs["new_body"]
    }
    
    # Make the PATCH request
    response = requests.patch(url, json=payload, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None if the response is empty (204 No Content), otherwise return the decoded JSON
    if not data:
        return None
    
    return data