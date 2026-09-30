import requests
import json

def solve(inputs):
    """
    Submits a new product to DummyJSON API.
    
    Args:
        inputs (dict): Dictionary containing 'new_description' and 'new_title'.
        
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
        
    Raises:
        requests.RequestException: If the HTTP request fails.
    """
    url = "https://dummyjson.com/products/add"
    
    payload = {
        "title": inputs["new_title"],
        "description": inputs["new_description"]
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 201:
        # Successful creation usually returns an empty body for this endpoint
        return None
    elif response.status_code in [200, 400]:
        # Return decoded JSON for other successful or client error responses
        try:
            return response.json()
        except json.JSONDecodeError:
            raise requests.RequestException(f"Failed to decode JSON response: {response.text}")
    else:
        raise requests.RequestException(f"HTTP Error: {response.status_code} - {response.reason}")