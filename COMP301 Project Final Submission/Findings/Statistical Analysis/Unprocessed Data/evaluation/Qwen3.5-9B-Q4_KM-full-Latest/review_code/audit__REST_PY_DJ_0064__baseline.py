import requests

def solve(inputs):
    """
    Submits a new product to DummyJSON API.
    
    Args:
        inputs (dict): A dictionary containing 'new_description' and 'new_title'.
        
    Returns:
        None if the request is successful (empty response).
        The decoded JSON response otherwise.
        
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    
    payload = {
        "title": inputs["new_title"],
        "body": inputs["new_description"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to submit product. Status code: {response.status_code}")
    
    return None