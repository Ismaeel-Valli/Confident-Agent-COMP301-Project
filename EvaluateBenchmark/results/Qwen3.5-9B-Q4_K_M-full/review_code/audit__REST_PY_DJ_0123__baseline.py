import requests

def solve(inputs):
    """
    Updates selected fields of a product in DummyJSON API.
    
    Args:
        inputs (dict): A dictionary containing:
            - resource_id (str): Identifier of the product to update.
            - new_category (str): New value for the category attribute.
    
    Returns:
        None if the response is empty (successful update).
        The decoded JSON response otherwise.
    
    Raises:
        Exception: If the HTTP response indicates an error (non-2xx status code).
    """
    resource_id = inputs['resource_id']
    new_category = inputs['new_category']
    
    url = f"https://dummyjson.com/products/{resource_id}"
    payload = {
        "category": new_category
    }
    
    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update product: HTTP {response.status_code}, Body: {response.text}")
    
    return None