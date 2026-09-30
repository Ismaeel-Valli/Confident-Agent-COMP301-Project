import requests

def solve(inputs):
    """
    Retrieve one page of users from DummyJSON with pagination and sorting.
    
    Args:
        inputs (dict): Must contain:
            - results_to_skip (int): Number of results to skip for pagination.
            - sort_field (str): Field used for ordering the results.
    
    Returns:
        list: Decoded JSON response containing user data, or None if empty.
    
    Raises:
        Exception: If HTTP response is unsuccessful (non-2xx status code).
    """
    base_url = "https://dummyjson.com/users"
    params = {
        "skip": inputs["results_to_skip"],
        "limit": 1,  # Retrieve one page of users
        "sort_by": inputs["sort_field"]
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        return data.get("users", None)
    else:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")