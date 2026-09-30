import requests

def solve(inputs):
    """
    Lists issue comments for a specific GitHub repository issue using the GitHub REST API.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git extension).
            - issue_number (int): The number that identifies the issue.
            - since (str, optional): ISO 8601 timestamp to filter comments updated after this time.
            - page_size (int, optional): Number of results per page (max 100).
            - credential (dict): Caller-supplied credentials (assumed to have necessary permissions).
    
    Returns:
        list or None: Decoded JSON response as a list of comments, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    issue_number = inputs["issue_number"]
    since = inputs.get("since")
    page_size = min(inputs.get("page_size", 30), 100)
    credential = inputs["credential"]

    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "GitHub-REST-API-Client"
    }

    params = {}
    if since:
        params["since"] = since
    if page_size != 30:  # Only add if different from default
        params["per_page"] = page_size

    auth_token = credential.get("token") or credential.get("access_token")
    if not auth_token:
        raise ValueError("Credential token is missing.")

    headers["Authorization"] = f"Bearer {auth_token}"

    all_comments = []
    page = 1

    while True:
        params["page"] = page
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch issue comments. Status code: {response.status_code}, Response: {response.text}")

        data = response.json()
        if not data:
            return None
        
        all_comments.extend(data)
        
        # Check for pagination
        link_header = response.headers.get("Link", "")
        if "rel=\"next\"" not in link_header:
            break
        
        page += 1

    return all_comments