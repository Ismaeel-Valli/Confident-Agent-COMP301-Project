import requests

def solve(inputs):
    """
    Deletes a product by identifier using DummyJSON API.
    
    Args:
        inputs (dict): Dictionary containing 'resource_id' key with the product identifier.
        
    Returns:
        None if deletion is successful (empty response).
        
    Raises:
        Exception for unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    
    # DummyJSON delete endpoint pattern: https://dummyjson.com/products/id/{id}
    url = f"https://dummyjson.com/products/id/{resource_id}"
    
    response = requests.delete(url)
    
    if response.status_code == 200:
        return None
    else:
        raise Exception(f"Failed to delete product. HTTP Status Code: {response.status_code}, Response: {response.text}")