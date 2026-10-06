import requests

def solve(inputs):
    """
    Submits a new photo to JSONPlaceholder using the provided inputs dictionary.
    
    Args:
        inputs (dict): A dictionary containing 'new_title' for the photo's title attribute.
        
    Returns:
        str or None: The response's title value if present, otherwise None for a successful empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    url = "https://jsonplaceholder.typicode.com/photos"
    
    # Prepare the payload with the new_title from inputs
    payload = {
        "title": inputs.get("new_title")
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code} - {response.text}")
    
    # Check if the response is empty (no title in JSON body)
    data = response.json()
    
    if not data or "title" not in data:
        return None
    
    return data["title"]