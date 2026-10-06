import requests

def solve(inputs):
    """
    Retrieves one page of posts from DummyJSON based on provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - result_limit (int): Maximum number of results to return.
            - sort_field (str): Field used for ordering the results.
    
    Returns:
        list or None: The decoded JSON response as a list of posts, or None if the response is empty.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/posts"
    
    params = {
        "_limit": inputs["result_limit"],
        "_sort": inputs["sort_field"]
    }
    
    response = requests.get(f"{base_url}{endpoint}", params=params)
    
    if response.status_code != 200:
        raise requests.exceptions.RequestException(f"HTTP error occurred: {response.status_code}")
    
    data = response.json()
    
    return data if data else None