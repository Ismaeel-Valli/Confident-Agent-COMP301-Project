import requests

def solve(inputs):
    """
    Retrieves one page of users from DummyJSON based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - sort_field (str): Field used for ordering the results.
    
    Returns:
        list or None: The decoded JSON response as a list of users, or None if the response is empty.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP response status code indicates an error.
    """
    base_url = "https://dummyjson.com/users"
    
    params = {
        "limit": inputs["result_limit"],
        "sort": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    
    # Raise an exception for unsuccessful HTTP responses (status code outside 200-299)
    response.raise_for_status()
    
    data = response.json()
    
    # Return None if the users array is empty
    if not data.get("users"):
        return None
    
    return data["users"]