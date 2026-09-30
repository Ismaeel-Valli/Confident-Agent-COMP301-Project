import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to include.
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://dummyjson.com/products"
    params = {
        "include_fields": inputs["included_fields"],
        "limit": 1
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            # Return None for successful empty response (products array is empty)
            if not data.get("products"):
                return None
            return data
        else:
            raise Exception(f"HTTP error {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")