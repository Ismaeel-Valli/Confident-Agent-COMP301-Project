import requests

def solve(inputs):
    """
    Retrieve one page of posts from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - sort_field (str): Field used for ordering the results.
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/posts"
    params = {
        "limit": inputs["result_limit"],
        "sort": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: status code {response.status_code}")
    
    data = response.json()
    
    return data if data else None