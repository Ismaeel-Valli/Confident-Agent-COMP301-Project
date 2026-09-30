import requests

def solve(inputs):
    """
    Submit a new product to DummyJSON and return the title from the response,
    or None if the title attribute is absent. Return None for a successful empty response.
    Raise an exception for an unsuccessful HTTP response.
    
    Args:
        inputs (dict): Must contain 'new_description' and 'new_title'.
        
    Returns:
        str or None: The title from the response, or None if absent or on empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://dummyjson.com/products/add"
    
    payload = {
        "description": inputs["new_description"],
        "title": inputs["new_title"]
    }
    
    try:
        response = requests.post(base_url, json=payload)
        
        if response.status_code >= 400:
            raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
        
        data = response.json()
        
        # Check for empty response (no products array or empty array)
        if not data.get("products") or len(data["products"]) == 0:
            return None
        
        # Return the title from the first product in the response
        if "title" in data["products"][0]:
            return data["products"][0]["title"]
        else:
            return None
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")