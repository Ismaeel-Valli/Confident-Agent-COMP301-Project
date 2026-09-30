import requests

def solve(inputs):
    """
    Fetches forks of a GitHub repository using the GitHub REST API.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - sort (str): The sort order for the results.
            - page_size (int): Number of results per page (max 100).
            - page (int): Page number to fetch.
            - credential (str): Bearer token or OAuth token for authentication.
    
    Returns:
        list or None: Decoded JSON response as a list, or None if the response is empty.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code indicates an error.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    sort_order = inputs["sort"]
    page_size = inputs["page_size"]
    page_number = inputs["page"]
    credential = inputs["credential"]

    url = f"https://api.github.com/repos/{owner}/{repo}/forks"
    
    params = {
        "sort": sort_order,
        "per_page": page_size,
        "page": page_number
    }

    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Request failed with status code: {response.status_code}")

    data = response.json()
    
    return data if data else None