import requests

def solve(inputs):
    """
    Lists issue comments for a specific GitHub repository issue using the GitHub REST API.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - issue_number (int): The number that identifies the issue.
            - since (str, optional): ISO 8601 timestamp to filter comments updated after this time.
            - page_size (int, optional): Number of results per page (max 100).
            - credential (dict): Caller-supplied credentials (e.g., token or auth headers).
    
    Returns:
        list or None: Decoded JSON response as a list of comments, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    issue_number = inputs["issue_number"]
    since = inputs.get("since")
    page_size = inputs.get("page_size", 30)
    credential = inputs["credential"]

    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Add authentication if provided (assuming token in 'token' key or similar structure)
    if "token" in credential:
        headers["Authorization"] = f"Bearer {credential['token']}"
    elif "username" in credential and "password" in credential:
        headers["Authorization"] = f"Basic {credential['username']}:{'*' * len(credential['password'])}"

    params = {"per_page": page_size}
    if since:
        params["since"] = since

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    return None if not data else data