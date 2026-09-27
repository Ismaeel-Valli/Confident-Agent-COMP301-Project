import requests

def solve(inputs):
    """
    Updates selected fields of a product in DummyJSON API.
    
    Args:
        inputs (dict): Contains 'resource_id' (product ID) and 'new_category' (new category value).
        
    Returns:
        str or None: The response's 'id' value if present, otherwise None for successful empty responses.
        
    Raises:
        Exception: If the HTTP response is unsuccessful (status code not in 2xx range).
    """
    resource_id = inputs.get('resource_id')
    new_category = inputs.get('new_category')
    
    # Construct the URL to update the product
    url = f"https://dummyjson.com/products/{resource_id}"
    
    # Prepare the payload for the PATCH request
    payload = {
        "category": new_category
    }
    
    # Send the PATCH request
    response = requests.patch(url, json=payload)
    
    # Check if the response is successful (2xx status code)
    if response.status_code < 300:
        # If the response is empty or doesn't contain an 'id' field, return None
        if not response.json() or 'id' not in response.json():
            return None
        return response.json()['id']
    else:
        raise Exception(f"Failed to update product. HTTP status code: {response.status_code}")