import requests

def solve(inputs):
    """
    Retrieve one page of todos from DummyJSON with specified limit and fields.
    
    Args:
        inputs (dict): Dictionary containing:
            - result_limit (int): Maximum number of results to return
            - included_fields (str): Comma-separated list of fields to include
    
    Returns:
        dict or None: Decoded JSON response, or None for empty successful response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://dummyjson.com/todos"
    
    # Parse included_fields
    if inputs.get("included_fields"):
        fields_list = [f.strip() for f in inputs["included_fields"].split(",")]
        params = {
            "limit": inputs["result_limit"],
            "fields": ",".join(fields_list)
        }
    else:
        params = {
            "limit": inputs["result_limit"]
        }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Return None for empty successful response (no todos)
    if not data.get("todos") or len(data["todos"]) == 0:
        return None
    
    return data