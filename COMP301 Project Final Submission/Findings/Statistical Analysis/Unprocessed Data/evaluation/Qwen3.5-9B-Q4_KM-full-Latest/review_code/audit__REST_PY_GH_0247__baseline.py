import requests

def solve(inputs):
    """
    Fetches the list of forks for a given GitHub repository using the REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - sort (str): The sort order for the results.
            - page_size (int): Number of results per page (max 100).
            - page (int): Page number to fetch.
            - credential (dict): Caller-supplied credentials (assumed valid).
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is successfully empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    sort_order = inputs["sort"]
    page_size = inputs["page_size"]
    page_number = inputs["page"]
    credential = inputs["credential"]

    # Construct the API URL for listing forks
    url = f"https://api.github.com/repos/{owner}/{repo}/forks"
    
    # Build query parameters
    params = {
        "sort": sort_order,
        "per_page": page_size,
        "page": page_number
    }

    # Prepare headers with authentication (assuming credential contains token or username/password)
    headers = {}
    if "token" in credential:
        headers["Authorization"] = f"Bearer {credential['token']}"
    elif "username" in credential and "password" in credential:
        import base64
        auth_string = f"{credential['username']}:{credential['password']}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        headers["Authorization"] = f"Basic {encoded_auth}"

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch forks. HTTP Status: {response.status_code}, Response: {response.text}")

    json_response = response.json()

    # Return None for a successful empty response (e.g., no forks found)
    if not json_response:
        return None

    return json_response