import requests

def solve(inputs):
    """
    Lists repositories starred by a user via GitHub REST API.
    
    Args:
        inputs (dict): Contains 'username', 'sort', 'page_size', and 'credential'.
        
    Returns:
        list or None: Decoded JSON response as a list of repos, or None if empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    username = inputs["username"]
    sort = inputs["sort"]
    page_size = inputs["page_size"]
    credential = inputs["credential"]
    
    url = f"https://api.github.com/users/{username}/starred"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {credential}"
    }
    
    params = {
        "per_page": page_size,
        "sort": sort
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch starred repositories. Status code: {response.status_code}, Response: {response.text}")
    
    data = response.json()
    
    return None if len(data) == 0 else data