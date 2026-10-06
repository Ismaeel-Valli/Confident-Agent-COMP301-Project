import requests

def solve(inputs):
    """
    Fetches forks of a GitHub repository using the GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository (without .git).
            - sort (str): The sort order for the results.
            - page_size (int): Number of results per page (max 100).
            - page (int): Page number to fetch.
            - credential (str): Bearer token or OAuth token for authentication.
    
    Returns:
        list | None: Decoded JSON response as a list, or None if the response is empty.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code indicates an error.
        Exception: For other unexpected errors during the request.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    sort_order = inputs["sort"]
    page_size = inputs["page_size"]
    page_number = inputs["page"]
    credential = inputs["credential"]

    url = f"https://api.github.com/repos/{owner}/{repo}/forks"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    params = {
        "sort": sort_order,
        "per_page": page_size,
        "page": page_number
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        # Return None for a successful empty response
        if not data:
            return None
            
        return data
        
    except requests.exceptions.HTTPError as e:
        raise e
    except Exception as e:
        raise Exception(f"An error occurred while fetching forks: {str(e)}")