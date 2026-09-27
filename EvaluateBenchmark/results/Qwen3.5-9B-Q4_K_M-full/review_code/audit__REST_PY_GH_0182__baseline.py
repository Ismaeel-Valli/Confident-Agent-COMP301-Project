import requests
from urllib.parse import urlencode

def solve(inputs):
    """
    Lists issue comments for a specific GitHub repository issue using the REST API.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - issue_number (int): The issue number.
            - since (str, optional): ISO 8601 timestamp to filter comments updated after this time.
            - page_size (int, optional): Number of results per page (max 100).
            - credential (dict): Contains authentication details (e.g., token or username/password).
    
    Returns:
        dict or None: Decoded JSON response if successful; None for an empty list.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    issue_num = inputs["issue_number"]
    since = inputs.get("since")
    page_size = inputs.get("page_size", 30)  # Default to 30 if not provided
    credential = inputs["credential"]
    
    base_url = "https://api.github.com"
    url = f"{base_url}/repos/{owner}/{repo}/issues/{issue_num}/comments"
    
    params = {}
    if since:
        params["since"] = since
    if page_size:
        params["per_page"] = min(page_size, 100)
    
    # Prepare headers with authentication
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    auth_type = credential.get("type", "token")
    
    if auth_type == "token":
        token = credential.get("token")
        headers["Authorization"] = f"Bearer {token}"
    elif auth_type == "basic":
        username = credential.get("username")
        password = credential.get("password")
        headers["Authorization"] = f"Basic {credentials_to_basic_auth(username, password)}"
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return None for empty list as per requirement
    return data if data else None

def credentials_to_basic_auth(username, password):
    """Helper to create Basic Auth string."""
    import base64
    cred_string = f"{username}:{password}"
    encoded_creds = base64.b64encode(cred_string.encode("utf-8")).decode("utf-8")
    return encoded_creds