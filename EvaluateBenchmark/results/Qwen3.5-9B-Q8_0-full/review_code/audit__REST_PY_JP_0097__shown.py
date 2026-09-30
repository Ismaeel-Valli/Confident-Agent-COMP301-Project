import requests

def solve(inputs):
    """
    Update a photo in JSONPlaceholder with a new URL.
    
    Args:
        inputs (dict): Dictionary containing:
            - resource_id (int): ID of the photo to update
            - new_url (str): New URL value for the photo's url attribute
    
    Returns:
        dict or None: Decoded JSON response if successful, None for empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs["resource_id"]
    new_url = inputs["new_url"]
    
    url = f"{base_url}/photos/{resource_id}"
    
    response = requests.put(url, json={"url": new_url})
    
    if response.status_code == 200:
        return None
    elif response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to update photo: {response.status_code} - {response.text}")