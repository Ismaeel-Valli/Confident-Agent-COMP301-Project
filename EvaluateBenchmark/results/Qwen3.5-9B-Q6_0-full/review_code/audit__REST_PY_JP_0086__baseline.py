import requests

def solve(inputs):
    """
    Submits a new user to JSONPlaceholder using the provided inputs dictionary.
    
    Args:
        inputs (dict): A dictionary containing 'new_name' for the name attribute.
        
    Returns:
        str or None: The response's name value if present, otherwise None.
                     Returns None for a successful empty response.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request is unsuccessful.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    # Prepare the payload from inputs
    payload = {
        "name": inputs.get("new_name")
    }
    
    try:
        response = requests.post(url, json=payload)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Check if the response is empty
        if not response.text.strip():
            return None
        
        # Try to parse the JSON response and extract the name
        try:
            data = response.json()
            return data.get("name")
        except ValueError:
            # If JSON parsing fails but we have content, check for 'name' in text
            if "name" in response.text:
                return None  # Fallback if structure is unexpected but name might be there
            return None
            
    except requests.exceptions.RequestException as e:
        raise e