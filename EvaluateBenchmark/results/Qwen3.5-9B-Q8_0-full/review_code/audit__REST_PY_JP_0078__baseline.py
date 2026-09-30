import requests

def solve(inputs):
    """
    Submits a new photo to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing 'new_title' for the photo title.
        
    Returns:
        str or None: The title value from the response, or None if absent or successful empty response.
        
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    
    # Prepare the payload for creating a new photo (posts endpoint in JSONPlaceholder)
    payload = {
        "title": inputs.get("new_title")
    }
    
    try:
        response = requests.post(f"{base_url}/photos", json=payload)
        
        # Raise an exception for unsuccessful HTTP responses
        response.raise_for_status()
        
        # Return the title value if present, otherwise None
        data = response.json()
        return data.get("title")
    
    except requests.RequestException as e:
        raise e