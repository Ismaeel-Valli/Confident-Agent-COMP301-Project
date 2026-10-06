import requests

def solve(inputs):
    """
    Submits a new product to DummyJSON API with provided category and title.
    
    Args:
        inputs (dict): Dictionary containing 'new_category' and 'new_title'.
        
    Returns:
        int or None: The ID of the created product, or None if response is empty.
        
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status).
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    
    payload = {
        "title": inputs["new_title"],
        "body": inputs.get("new_category", ""),  # Using category as body content since DummyJSON posts require body
        "userId": 1  # Assuming a valid user exists as per instructions
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code >= 400:
        raise Exception(f"Failed to create product. Status code: {response.status_code}")
        
    if response.json():
        return response.json().get("id")
    else:
        return None