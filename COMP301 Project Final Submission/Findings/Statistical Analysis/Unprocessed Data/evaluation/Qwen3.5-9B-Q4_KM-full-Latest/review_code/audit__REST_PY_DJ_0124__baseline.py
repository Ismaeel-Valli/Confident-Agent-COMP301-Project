import requests


def solve(inputs):
    """
    Submits a new product to DummyJSON API with provided category and title.
    
    Args:
        inputs (dict): Contains 'new_category' and 'new_title'.
        
    Returns:
        None if the request is successful (empty response body).
        The decoded JSON response if the server returns data.
        
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    
    payload = {
        "title": inputs["new_title"],
        "body": inputs["new_category"]  # Using category as body text since DummyJSON posts require 'body'
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to submit product. HTTP Status Code: {response.status_code}")
    
    # DummyJSON returns an empty body for POST requests on /posts
    if not response.text.strip():
        return None
    
    return response.json()