import requests

def solve(inputs):
    """
    Lists commits for a GitHub repository using the specified API version.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - page_size (int): Number of results per page (max 100).
            - credential (str): Caller-supplied credential (e.g., Bearer token or API key).
    
    Returns:
        dict or None: Decoded JSON response if commits exist, None for empty list.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    page_size = inputs["page_size"]
    credential = inputs["credential"]

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
        "Authorization": f"Bearer {credential}"
    }

    params = {"per_page": page_size}

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to list commits. HTTP status code: {response.status_code}, Response: {response.text}")

    data = response.json()
    
    # Return None for empty list as per requirement
    return None if not data else data