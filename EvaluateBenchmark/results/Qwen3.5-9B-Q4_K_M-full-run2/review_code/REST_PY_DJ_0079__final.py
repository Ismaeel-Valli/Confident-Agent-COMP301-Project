import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON, sorted by sort_field.
    
    Args:
        inputs (dict): Must contain 'sort_field' key with a string value.
        
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx).
    """
    base_url = "https://dummyjson.com"
    sort_field = inputs["sort_field"]
    
    url = f"{base_url}/posts?sort={sort_field}"
    
    response = requests.get(url)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    return data if data else None