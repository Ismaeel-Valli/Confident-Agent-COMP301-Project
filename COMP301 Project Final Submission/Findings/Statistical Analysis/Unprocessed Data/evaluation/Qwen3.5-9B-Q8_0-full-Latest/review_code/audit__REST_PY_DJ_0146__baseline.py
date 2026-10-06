import requests

def solve(inputs):
    """
    Retrieves one page of posts from DummyJSON based on provided sorting parameters.
    
    Args:
        inputs (dict): A dictionary containing:
            - sort_field (str): The field to sort by.
            - sort_direction (str): The direction to sort ('asc' or 'desc').
    
    Returns:
        list or None: The decoded JSON response as a list of posts, or None if the response is empty.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com/posts"
    
    params = {
        "_limit": 1,
        "_sort": inputs["sort_field"],
        "_order": inputs["sort_direction"]
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")
    
    data = response.json()
    
    return data if data else None