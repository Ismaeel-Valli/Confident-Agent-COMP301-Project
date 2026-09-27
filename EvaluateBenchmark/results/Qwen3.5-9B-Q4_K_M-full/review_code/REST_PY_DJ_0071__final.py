import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON.
    
    Args:
        inputs (dict): Dictionary containing:
            - 'included_fields': str, comma-separated list of fields to return
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com"
    endpoint = "/todos"
    
    # Parse included_fields from comma-separated string
    included_fields = inputs.get("included_fields", "")
    if included_fields:
        fields_list = [f.strip() for f in included_fields.split(",")]
    else:
        fields_list = []
    
    # Build query parameters
    params = {}
    if fields_list:
        params["fields"] = ",".join(fields_list)
    
    # Make the request
    response = requests.get(f"{base_url}{endpoint}", params=params)
    
    # Check for unsuccessful HTTP response
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    # Decode and return JSON response
    data = response.json()
    
    # Return None for successful empty response (empty todos array)
    if not data.get("todos") or len(data["todos"]) == 0:
        return None
    
    return data