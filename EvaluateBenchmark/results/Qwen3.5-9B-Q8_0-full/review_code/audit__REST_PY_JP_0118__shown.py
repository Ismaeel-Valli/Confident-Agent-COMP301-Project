import requests

def solve(inputs):
    """
    Submit a new album to JSONPlaceholder using the provided title and user ID.
    
    Args:
        inputs (dict): Must contain 'new_title' (str) and 'new_user_identifier' (int).
        
    Returns:
        str or None: The title from the response, or None if absent or response is empty.
        
    Raises:
        Exception: If the HTTP response indicates failure (status code not 200-299).
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/albums"
    
    url = f"{base_url}{endpoint}"
    
    payload = {
        "title": inputs["new_title"],
        "userId": inputs["new_user_identifier"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failed to create album. Status code: {response.status_code}")
    
    data = response.json()
    
    if not data:
        return None
    
    return data.get("title")