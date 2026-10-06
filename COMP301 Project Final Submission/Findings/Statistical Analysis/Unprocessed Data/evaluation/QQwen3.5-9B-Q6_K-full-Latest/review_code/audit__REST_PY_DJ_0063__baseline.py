import requests

def solve(inputs):
    """
    Deletes a product by identifier from DummyJSON API.
    
    Args:
        inputs (dict): Dictionary containing 'resource_id' key with the product identifier.
        
    Returns:
        bool or None: The 'isDeleted' value from the response, or None if absent or for successful empty response.
        
    Raises:
        requests.exceptions.HTTPError: If the HTTP response is unsuccessful.
    """
    resource_id = inputs.get('resource_id')
    
    # Construct the API endpoint URL for deleting a product by ID
    url = f"https://dummyjson.com/products/{resource_id}"
    
    try:
        # Send DELETE request to the API
        response = requests.delete(url)
        
        # Raise an exception for unsuccessful HTTP responses (status code not in 2xx range)
        response.raise_for_status()
        
        # Check if the response is empty (successful deletion often returns empty body)
        if not response.text:
            return None
        
        # Parse the JSON response
        data = response.json()
        
        # Return the 'isDeleted' value if present, otherwise None
        return data.get('isDeleted')
        
    except requests.exceptions.HTTPError as e:
        raise e