import requests

def solve(inputs):
    """
    Look up countries by exact match on their currency code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - "value": The currency code to match exactly (e.g., "USD", "EUR")
            - "credential": Caller-supplied credential with necessary permissions
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5"
    
    # Construct the API endpoint to search by currency code
    url = f"{base_url}/search?currency={inputs['value']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        # Raise an exception for unsuccessful HTTP responses (4xx, 5xx)
        response.raise_for_status()
        
        # Decode the JSON response
        data = response.json()
        
        # Return None for successful empty response
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Unsuccessful HTTP response: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")