import requests

def solve(inputs):
    """
    List issue comments for a GitHub repository using the REST API version 2026-03-10.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git extension).
            - issue_number (int): The number that identifies the issue.
            - since (str, optional): Only show results that were last updated after the given time.
            - page (int, optional): The page number of the results to fetch.
            - credential (str): The caller-supplied authentication token.
    
    Returns:
        list or None: A list of issue comments if found, or None for a successful empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    # Base URL for GitHub REST API version 2026-03-10
    base_url = "https://api.github.com"
    
    # Construct the endpoint URL for listing issue comments
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    issue_number = inputs["issue_number"]
    
    url = f"{base_url}/repos/{owner}/{repo}/issues/{issue_number}/comments"
    
    # Prepare headers with authentication
    headers = {
        "Authorization": f"token {inputs['credential']}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Prepare query parameters
    params = {}
    if "since" in inputs:
        params["since"] = inputs["since"]
    if "page" in inputs:
        params["page"] = inputs["page"]
    
    # Make the GET request
    response = requests.get(url, headers=headers, params=params)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode and return the JSON response
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data