import requests

def solve(inputs):
    """
    Updates selected fields of a product in DummyJSON API.
    
    Args:
        inputs (dict): Contains 'resource_id' (product ID) and 'new_category' (new category value).
        
    Returns:
        str or None: The response's id value if present, otherwise None for successful empty response.
        Raises: Exception for unsuccessful HTTP responses.
    """
    resource_id = inputs['resource_id']
    new_category = inputs['new_category']
    
    # Base URL for DummyJSON API (using the PUT endpoint to update a product)
    url = f"https://dummyjson.com/products/{resource_id}"
    
    # Prepare the payload with only the field we want to update
    payload = {
        "category": new_category
    }
    
    try:
        response = requests.put(url, json=payload)
        
        # Raise an exception for unsuccessful HTTP responses (4xx or 5xx)
        response.raise_for_status()
        
        # Check if the response is empty (no content)
        if not response.text.strip():
            return None
        
        # Parse the JSON response
        data = response.json()
        
        # Return the id value if present, otherwise None
        return data.get('id')
        
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")