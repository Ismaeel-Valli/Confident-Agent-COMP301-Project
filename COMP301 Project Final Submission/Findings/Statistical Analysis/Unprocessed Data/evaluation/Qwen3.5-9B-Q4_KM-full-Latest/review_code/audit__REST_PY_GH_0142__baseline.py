import requests

def solve(inputs):
    """
    Lists commits for a GitHub repository filtered by author.
    
    Args:
        inputs (dict): Contains:
            - repository_owner (str): Account owner of the repository.
            - repository_name (str): Name of the repository (without .git).
            - author (str): GitHub username or email to filter commits.
            - credential (dict): Caller-supplied credentials (e.g., token in 'token' key).
    
    Returns:
        list[dict] | None: Decoded JSON response as a list of commit objects, 
                           or None if the response is an empty list.
    
    Raises:
        Exception: If the HTTP response indicates failure (non-2xx status).
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    author = inputs["author"]
    credential = inputs["credential"]

    # Construct the API URL for listing commits with author filter
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    
    # Prepare headers with authentication
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {credential.get('token', '')}"
    }

    params = {"author": author}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to list commits: HTTP {response.status_code}, Response: {response.text}")

    data = response.json()

    # Return None for an empty successful response
    return data if data else None