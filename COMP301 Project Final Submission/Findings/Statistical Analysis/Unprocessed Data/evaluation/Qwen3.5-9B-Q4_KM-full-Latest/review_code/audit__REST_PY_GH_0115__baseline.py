import requests

def solve(inputs):
    """
    Lists labels for a GitHub repository using the REST API (version 2026-03-10).
    
    Args:
        inputs (dict): A dictionary containing:
            - 'repository_owner' (str): The account owner of the repository.
            - 'repository_name' (str): The name of the repository (without .git extension).
            - 'page' (int): The page number of results to fetch.
            - 'credential' (dict): Caller-supplied credential with necessary permissions.
    
    Returns:
        dict or None: Decoded JSON response if successful, or None for an empty response.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs['repository_owner']
    repo = inputs['repository_name']
    page = inputs['page']
    credential = inputs['credential']
    
    # Construct the API URL for listing labels (v3 endpoint, as v4 GraphQL is not REST)
    url = f"https://api.github.com/repos/{owner}/{repo}/labels?page={page}"
    
    headers = {
        "Accept": "application/vnd.github+json"
    }
    
    # Attach credentials to the request
    if 'token' in credential:
        headers["Authorization"] = f"Bearer {credential['token']}"
    elif 'username' in credential and 'password' in credential:
        auth = requests.auth.HTTPBasicAuth(credential['username'], credential['password'])
        response = requests.get(url, headers=headers, auth=auth)
    else:
        # Fallback if no standard auth is found, though the problem assumes valid credentials
        raise ValueError("Credential must contain 'token' or both 'username' and 'password'.")

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for a successful empty response (empty list of labels)
    if not data:
        return None
    
    return data