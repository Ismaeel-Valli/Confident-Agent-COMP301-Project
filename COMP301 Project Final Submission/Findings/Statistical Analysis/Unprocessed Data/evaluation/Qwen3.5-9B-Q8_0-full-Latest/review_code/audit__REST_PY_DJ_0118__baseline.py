import requests

def solve(inputs):
    """
    Submits a new user to DummyJSON API using provided inputs.
    
    Args:
        inputs (dict): Dictionary containing 'new_firstName' and 'new_phone'.
        
    Returns:
        None if the response is empty (successful).
        Decoded JSON response otherwise.
        
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    url = "https://jsonplaceholder.typicode.com/users"
    
    # Prepare the payload with required fields and additional necessary fields
    payload = {
        "name": inputs["new_firstName"],
        "phone": inputs["new_phone"]
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code != 201:
            raise Exception(f"Failed to create user. Status code: {response.status_code}")
        
        # Check if the response is empty
        if not response.text.strip():
            return None
            
        return response.json()
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")