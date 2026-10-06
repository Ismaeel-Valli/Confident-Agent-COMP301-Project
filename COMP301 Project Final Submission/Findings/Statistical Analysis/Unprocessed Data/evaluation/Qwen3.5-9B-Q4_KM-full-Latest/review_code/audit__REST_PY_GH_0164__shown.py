def solve(inputs):
    """
    List stargazers for a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - page_size (int): The number of results per page (max 100).
            - page (int): The page number of the results to fetch.
            - credential (str): The caller-supplied credential (assumed to have necessary permissions).
    
    Returns:
        dict or None: The decoded JSON response, or None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    import requests
    
    # Construct the API URL with the specified version 2026-03-10
    base_url = "https://api.github.com"
    url = f"{base_url}/repos/{inputs['repository_owner']}/{inputs['repository_name']}/stargazers"
    
    # Prepare headers with the credential
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {inputs['credential']}"
    }
    
    # Prepare query parameters
    params = {
        "per_page": inputs["page_size"],
        "page": inputs["page"]
    }
    
    # Make the request
    response = requests.get(url, headers=headers, params=params)
    
    # Raise an exception for unsuccessful HTTP responses
    response.raise_for_status()
    
    # Decode the JSON response
    data = response.json()
    
    # Return None for a successful empty response
    if not data:
        return None
    
    return data