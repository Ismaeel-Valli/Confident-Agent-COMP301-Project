import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON, sorted by a specified field and direction.
    
    Args:
        inputs (dict): Must contain:
            - 'sort_field': str, the field to sort by
            - 'sort_direction': str, either 'asc' or 'desc'
    
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx).
    """
    base_url = "https://dummyjson.com/posts"
    params = {
        "sort": inputs["sort_field"],
        "order": inputs["sort_direction"]
    }
    
    response = requests.get(base_url, params=params)
    
    if not (200 <= response.status_code < 300):
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Return None for a successful empty response
    if not data.get("posts"):
        return None
    
    return data