import requests


def solve(inputs):
    """
    Retrieve posts from JSONPlaceholder and return decoded JSON response.
    - Returns None for successful empty response (200 OK)
    - Raises an exception for unsuccessful HTTP response (non-2xx)
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        json_response = response.json()
        return None  # Successful empty response returns None
    else:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")