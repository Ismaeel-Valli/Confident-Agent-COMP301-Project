import requests

def solve(inputs):
    """
    Submits a new photo to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing 'new_title' for the photo title.
        
    Returns:
        str or None: The response's title value if present, otherwise None.
                     Returns None for a successful empty response.
                     
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    new_title = inputs.get('new_title')
    
    # Endpoint to add a photo (posts endpoint in JSONPlaceholder)
    url = f"{base_url}/photos"
    
    payload = {
        "title": new_title
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code != 201:
        raise requests.RequestException(f"Failed to submit photo. Status code: {response.status_code}")
    
    # Check if the response is empty or doesn't contain a title
    data = response.json()
    
    if not data or 'title' not in data:
        return None
    
    return data['title']