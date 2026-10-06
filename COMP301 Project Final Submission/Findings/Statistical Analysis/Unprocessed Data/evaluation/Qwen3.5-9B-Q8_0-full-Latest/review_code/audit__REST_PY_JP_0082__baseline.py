import requests

def solve(inputs):
    """
    Submits a new todo to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing 'new_title' for the todo title.
        
    Returns:
        str or None: The title of the created todo, or None if the response is empty.
        
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    new_title = inputs.get('new_title')
    
    url = f"{base_url}/todos"
    payload = {"title": new_title}
    
    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    
    if response.status_code == 201:
        data = response.json()
        return data.get('title')
    elif response.status_code == 200 and not response.text.strip():
        return None
    else:
        # This case should theoretically be covered by raise_for_status, 
        # but handles unexpected success codes with empty body just in case.
        if not response.text.strip():
            return None
        raise Exception(f"Unexpected response status code: {response.status_code}")

# Example usage (not executed):
# inputs = {'new_title': 'Learn Python'}
# result = solve(inputs)
# print(result)