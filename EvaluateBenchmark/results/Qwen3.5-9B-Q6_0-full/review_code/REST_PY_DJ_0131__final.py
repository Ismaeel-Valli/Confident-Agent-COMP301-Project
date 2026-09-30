import requests

def solve(inputs):
    """
    Retrieve one page of products from DummyJSON with specified fields and sorting.
    
    Args:
        inputs (dict): Dictionary containing:
            - included_fields (str): Comma-separated list of fields to include
            - sort_field (str): Field to sort by
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/products"
    
    # Build query parameters
    params = {}
    
    # Add include parameter if included_fields is provided
    if inputs.get("included_fields"):
        fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
        params["include"] = ",".join(fields_list)
    
    # Add sort parameter if sort_field is provided
    if inputs.get("sort_field"):
        params["sort"] = inputs["sort_field"]
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response (no products)
    if not data.get("products") or len(data["products"]) == 0:
        return None
    
    return data