import requests

def solve(inputs):
    """
    Submits a new comment to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing 'new_name' for the name attribute.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    new_name = inputs.get('new_name')
    
    url = "https://jsonplaceholder.typicode.com/posts"
    payload = {
        "title": "foo",
        "body": "bar",
        "userId": 1,
        "name": new_name
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 201:
        return None
    elif response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")