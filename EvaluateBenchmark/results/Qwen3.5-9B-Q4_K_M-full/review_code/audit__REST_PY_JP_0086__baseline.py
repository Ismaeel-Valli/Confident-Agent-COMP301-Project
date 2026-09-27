import requests

def solve(inputs):
    """
    Submits a new user to JSONPlaceholder using the provided name.
    
    Args:
        inputs (dict): A dictionary containing 'new_name' for the user's name.
        
    Returns:
        str or None: The response's 'name' value if present, otherwise None for a successful empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (status code outside 2xx/3xx range).
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    payload = {
        "name": inputs.get("new_name")
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    # Raise an exception for unsuccessful HTTP responses (non-2xx/3xx)
    response.raise_for_status()
    
    # Check if the response is empty
    if not response.text:
        return None
    
    # Try to parse the JSON response and extract the 'name' attribute
    try:
        data = response.json()
        name = data.get("name")
        return name if name is not None else None
    except ValueError:
        # If response is not valid JSON, treat as empty or error
        return None