import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with specified fields and sorting.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to include
            - sort_field (str): Field to sort by
    
    Returns:
        dict or None: Decoded JSON response, or None if empty
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/users"
    
    # Parse included_fields
    fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
    
    # Build query parameters
    params = {
        "fields": ",".join(fields_list),
        "sort": inputs["sort_field"]
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        
        data = response.json()
        
        # Return None if the users array is empty
        if not data.get("users"):
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")