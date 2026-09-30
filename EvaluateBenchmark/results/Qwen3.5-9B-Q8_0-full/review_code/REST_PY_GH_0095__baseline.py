import requests

def solve(inputs):
    """
    Lists repository tags for GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - page_size (int): The number of results per page (max 100).
            - credential (str): The caller-supplied credential (e.g., Bearer token or OAuth token).
    
    Returns:
        list | None: A list of decoded JSON responses for each page, or None if the response is empty.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code indicates an error.
    """
    repository_owner = inputs["repository_owner"]
    repository_name = inputs["repository_name"]
    page_size = inputs["page_size"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{repository_owner}/{repository_name}/tags"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {credential}"
    }
    
    params = {
        "per_page": page_size
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Request failed with status code: {response.status_code}")
    
    data = response.json()
    
    # GitHub API returns paginated results. We need to fetch all pages.
    # However, the problem statement says "Return the decoded JSON response." 
    # and "Return None for a successful empty response."
    # It doesn't explicitly ask to paginate through all pages, but typically "list" implies getting all items.
    # Given the constraints of a single function call without explicit pagination logic requested in the prompt's core requirement (which focuses on the initial request structure), 
    # and the instruction "Return the decoded JSON response", I will return the first page's data as per standard API interaction unless specified otherwise.
    # BUT, looking at the instruction "List repository tags", it implies getting all tags.
    # Since the function signature only takes inputs once, and we don't have a loop mechanism provided in the input, 
    # I will assume the task is to make the initial request and return that response. 
    # If the API returns multiple pages, this function would only return the first page.
    # However, to be thorough and "list" all tags, we should implement pagination.
    # Let's implement pagination to ensure all tags are listed as implied by "List repository tags".

    all_tags = []
    while True:
        if data is None or len(data) == 0:
            return None
        
        all_tags.extend(data)
        
        if not response.links.get("next"):
            break
            
        url = response.links["next"]["url"]
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f"Request failed with status code: {response.status_code}")
        data = response.json()

    return all_tags