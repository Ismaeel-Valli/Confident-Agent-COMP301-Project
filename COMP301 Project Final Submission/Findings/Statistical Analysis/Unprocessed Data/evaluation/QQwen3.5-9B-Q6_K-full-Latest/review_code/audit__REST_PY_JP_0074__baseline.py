import requests

def solve(inputs):
    """
    Submits a new album to JSONPlaceholder using the provided title.
    
    Args:
        inputs (dict): A dictionary containing 'new_title' for the album title.
        
    Returns:
        str or None: The title from the response if present, otherwise None.
                     Returns None for a successful empty response.
        
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/albums"  # Note: JSONPlaceholder typically uses /posts, but assuming custom endpoint as per prompt context or hypothetical extension
    
    # Prepare the payload
    payload = {
        "title": inputs.get("new_title")
    }
    
    try:
        response = requests.post(f"{base_url}{endpoint}", json=payload)
        
        # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        
        # Check if the response is empty
        if not response.text.strip():
            return None
        
        # Parse JSON response to get the title
        try:
            data = response.json()
            return data.get("title")
        except ValueError:
            # If response is not valid JSON but not empty, return None or handle as needed
            # Based on instructions, if attribute is absent in a non-empty response, we might need to decide.
            # However, the instruction says "Return only the response's title value, or None if that attribute is absent."
            # If it's not JSON, we can't easily get 'title'. Let's assume valid JSON structure for albums.
            return None
            
    except requests.RequestException as e:
        raise e