import requests

def solve(inputs):
    """
    Retrieves photos from JSONPlaceholder using the provided inputs (typically user_id).
    
    Args:
        inputs (dict): A dictionary containing 'user_id' to filter photos by user.
        
    Returns:
        list or None: The decoded JSON response as a list of photos, or None if the response is empty.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    user_id = inputs.get('user_id')
    
    url = f"{base_url}/photos?userId={user_id}"
    
    response = requests.get(url)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    
    data = response.json()
    
    if not data:
        return None
        
    return data