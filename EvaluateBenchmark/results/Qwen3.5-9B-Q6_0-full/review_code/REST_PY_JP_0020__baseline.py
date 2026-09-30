import requests

def solve(inputs):
    """
    Submits a new photo to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing 'new_title' for the photo title.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    url = "https://jsonplaceholder.typicode.com/photos"
    
    # Prepare the payload with the new title and other required fields
    payload = {
        "albumId": 1,
        "title": inputs["new_title"],
        "userId": 1
    }
    
    try:
        response = requests.post(url, json=payload)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Return None for a successful empty response
        if not response.text:
            return None
            
        # Return the decoded JSON response
        return response.json()
        
    except requests.exceptions.HTTPError as e:
        raise e
    except requests.exceptions.RequestException as e:
        raise e