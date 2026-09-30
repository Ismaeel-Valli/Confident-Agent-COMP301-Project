import requests

def solve(inputs):
    """
    Retrieves one page of posts from DummyJSON based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - results_to_skip (int): Number of results to skip.
            - included_fields (str): Comma-separated list of fields to include.
    
    Returns:
        dict or None: The decoded JSON response, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/posts"
    
    # Parse included_fields
    fields_list = [field.strip() for field in inputs["included_fields"].split(",")]
    
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,  # Retrieve one page (one result)
        "_fields": ",".join(fields_list)
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        if response.status_code == 200:
            data = response.json()
            # DummyJSON returns a list of posts directly in the root for /posts endpoint
            if not data:
                return None
            return data
        else:
            raise Exception(f"HTTP error occurred: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")