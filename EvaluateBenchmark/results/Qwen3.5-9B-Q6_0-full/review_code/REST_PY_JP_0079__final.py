import requests

def solve(inputs):
    """
    Retrieve a photo by identifier from JSONPlaceholder and return its title.
    
    Args:
        inputs (dict): Must contain 'resource_id' (int) for the photo ID.
        
    Returns:
        str or None: The photo's title, or None if absent or response is empty.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    resource_id = inputs.get('resource_id')
    if resource_id is None:
        raise ValueError("Missing 'resource_id' in inputs")
    
    url = "https://jsonplaceholder.typicode.com/photos"
    params = {"id": resource_id}
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raises exception for unsuccessful HTTP responses
    
    if response.status_code == 200:
        data = response.json()
        return data.get('title')
    else:
        raise Exception(f"HTTP error {response.status_code}: {response.text}")