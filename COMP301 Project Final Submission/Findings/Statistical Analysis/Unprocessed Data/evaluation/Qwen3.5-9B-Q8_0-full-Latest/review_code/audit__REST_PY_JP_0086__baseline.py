import requests

def solve(inputs):
    """
    Submits a new user to JSONPlaceholder using the provided name.
    
    Args:
        inputs (dict): A dictionary containing 'new_name' for the user's name.
        
    Returns:
        str or None: The name value from the response if present, otherwise None.
                     Returns None for a successful empty response.
        
    Raises:
        requests.RequestException: If the HTTP response is unsuccessful.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    # Prepare the payload with the new name
    payload = {
        "name": inputs.get("new_name")
    }
    
    try:
        response = requests.post(url, json=payload)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Check if the response content is empty
        if not response.text.strip():
            return None
        
        # Try to parse the JSON response and extract the name
        try:
            data = response.json()
            return data.get("name")
        except ValueError:
            # If JSON parsing fails, check if the raw text contains 'name'
            if "name" in response.text:
                # Simple heuristic to extract name if JSON is malformed but text exists
                start_idx = response.text.find('"name":') + len('"name":')
                end_idx = response.text.find(',"', start_idx)
                if end_idx == -1:
                    end_idx = response.text.find('"', start_idx)
                if end_idx != -1:
                    return response.text[start_idx:end_idx].strip()
            return None
            
    except requests.RequestException as e:
        raise e