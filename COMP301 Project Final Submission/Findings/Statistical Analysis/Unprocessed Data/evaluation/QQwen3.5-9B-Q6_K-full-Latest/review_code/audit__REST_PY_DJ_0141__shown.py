import requests

def solve(inputs):
    """
    Update selected fields of a product on DummyJSON.
    
    Args:
        inputs (dict): Must contain 'resource_id' and 'new_category'.
        
    Returns:
        str or None: The title from the updated product, or None if absent or response is empty.
        
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    new_category = inputs['new_category']
    
    url = "https://dummyjson.com/products/{id}".format(id=resource_id)
    payload = {"category": new_category}
    
    try:
        response = requests.put(url, json=payload)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            # DummyJSON returns the updated product directly in the response body for PUT
            title = data.get('title')
            return title if title is not None else None
        elif response.status_code == 204:
            return None
        else:
            raise Exception(f"Unexpected status code: {response.status_code}")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")