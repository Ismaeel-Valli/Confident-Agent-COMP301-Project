import requests

def solve(inputs):
    """
    List stargazers for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - repository_owner (str): The account owner of the repository
            - repository_name (str): The name of the repository without .git extension
            - page (int): The page number of results to fetch
            - credential (str): Caller-supplied authentication token
    
    Returns:
        list or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    # Build the API URL with version 2026-03-10
    base_url = "https://api.github.com"
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    page = inputs["page"]
    credential = inputs["credential"]
    
    # Construct the endpoint for listing stargazers
    url = f"{base_url}/repos/{repository_owner}/{repository_name}/stargazers"
    
    # Prepare headers with authentication
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {credential}"
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 200:
        raise Exception(f"GitHub API returned status code {response.status_code}: {response.text}")
    
    # Decode JSON response
    data = response.json()
    
    # Return None for empty successful response, otherwise return the data
    if len(data) == 0:
        return None
    
    return data