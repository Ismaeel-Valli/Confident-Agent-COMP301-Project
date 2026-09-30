import requests

def solve(inputs):
    """
    Submits a new user to DummyJSON API using provided inputs.
    
    Args:
        inputs (dict): Dictionary containing 'new_firstName' and other required fields.
        
    Returns:
        int or None: The ID of the created user, or None if response is empty.
        
    Raises:
        requests.exceptions.RequestException: If HTTP request fails.
    """
    # DummyJSON API endpoint for creating a new user
    url = "https://dummyjson.com/users/add"
    
    # Prepare the payload with the provided inputs
    payload = {
        "firstName": inputs.get("new_firstName"),
        # Include other required fields if available in inputs
        **{k: v for k, v in inputs.items() if k != "new_firstName"}
    }
    
    try:
        response = requests.post(url, json=payload)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Check if the response is empty
        if not response.text.strip():
            return None
        
        # Return the ID from the response
        try:
            data = response.json()
            return data.get("id")
        except ValueError:
            # If JSON parsing fails, return None
            return None
            
    except requests.exceptions.RequestException as e:
        raise e