import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON.
    
    Args:
        inputs (dict): Must contain:
            - result_limit (int): Maximum number of results to return.
            - sort_field (str): Field used for ordering the results.
    
    Returns:
        list or None: The decoded JSON response as a list, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    base_url = "https://dummyjson.com/users"
    params = {
        "limit": inputs["result_limit"],
        "sort_by": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    return data.get("users", None)