import requests

def solve(inputs):
    """
    Retrieves users from JSONPlaceholder API.
    
    Args:
        inputs (dict): A dictionary containing 'perPage' key for pagination.
        
    Returns:
        list or None: Decoded JSON response as a list, or None if empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    per_page = inputs.get('perPage', 10)
    
    url = f"{base_url}/users?_limit={per_page}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    if not data:
        return None
        
    return data