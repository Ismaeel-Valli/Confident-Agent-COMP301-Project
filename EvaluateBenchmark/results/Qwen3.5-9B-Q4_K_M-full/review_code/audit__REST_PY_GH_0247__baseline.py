import requests

def solve(inputs):
    """
    Lists forks for a given GitHub repository using the GitHub REST API.
    
    Parameters:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - sort (str): The sort order for the results.
            - page_size (int): Number of results per page (max 100).
            - page (int): Page number to fetch.
            - credential (dict): Caller-supplied credentials (e.g., token or auth headers).
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty but successful.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    sort = inputs["sort"]
    page_size = inputs["page_size"]
    page = inputs["page"]
    credential = inputs["credential"]

    # Construct the API URL for listing forks
    url = f"https://api.github.com/repos/{owner}/{repo}/forks"

    # Build query parameters
    params = {
        "sort": sort,
        "per_page": page_size,
        "page": page
    }

    # Prepare headers from credential (assuming it contains 'token' or similar)
    headers = {}
    if isinstance(credential, dict):
        token = credential.get("token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        else:
            # Fallback to basic auth if token is not present but username/password are
            user = credential.get("username")
            password = credential.get("password")
            if user and password:
                import base64
                auth_string = f"{user}:{password}"
                encoded_auth = base64.b64encode(auth_string.encode()).decode()
                headers["Authorization"] = f"Basic {encoded_auth}"

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"GitHub API request failed with status code {response.status_code}: {response.text}")

    data = response.json()

    # Return None for successful empty response
    if not data:
        return None

    return data