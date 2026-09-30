import requests

def solve(inputs):
    """
    Update a pull request on GitHub using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - pull_number (int): Pull request number to update
            - new_body (str): New body content for the pull request
            - credential (str): Bearer token for authentication
    
    Returns:
        dict or None: Decoded JSON response, or None if successful with empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Build the API URL for updating a pull request
    base_url = "https://api.github.com"
    version = "2026-03-10"
    
    # Construct the endpoint path
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    pr_number = inputs["pull_number"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    
    # Prepare headers with authentication
    credential = inputs["credential"]
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": f"application/vnd.github.{version}-preview+json",
        "Content-Type": "application/json"
    }
    
    # Prepare the payload
    data = {
        "body": inputs["new_body"]
    }
    
    # Make the PATCH request to update the pull request
    response = requests.patch(url, json=data, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    result = response.json()
    
    # Return None if the response is empty (successful update with no changes needed)
    if not result:
        return None
    
    return result