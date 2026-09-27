import requests

def solve(inputs):
    """
    List issue comments for a GitHub repository.
    
    Args:
        inputs (dict): Must contain:
            - repository_owner (str): Account owner of the repository
            - repository_name (str): Name of the repository (without .git)
            - issue_number (int): Issue number to fetch comments for
            - since (str, optional): ISO 8601 timestamp to filter comments updated after this time
            - credential (str): Bearer token for authentication
    
    Returns:
        list[dict]: Decoded JSON response containing issue comments.
                    Returns None if the response is empty.
    
    Raises:
        Exception: For unsuccessful HTTP responses (non-2xx status codes).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    issue_num = inputs["issue_number"]
    since = inputs.get("since")
    token = inputs["credential"]
    
    base_url = "https://api.github.com"
    url = f"{base_url}/repos/{owner}/{repo}/issues/{issue_num}/comments"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    params = {}
    if since:
        params["since"] = since
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data