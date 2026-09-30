import requests

def solve(inputs):
    """
    Update selected fields of a product on DummyJSON.
    
    inputs: dict with keys:
        - resource_id (int): ID of the product to update
        - new_description (str): New description value
    
    Returns:
        - int: The response's id if present
        - None: If response is empty or id is absent
        - Raises: Exception for unsuccessful HTTP responses
    """
    resource_id = inputs["resource_id"]
    new_description = inputs["new_description"]
    
    url = f"https://dummyjson.com/products/{resource_id}"
    payload = {
        "description": new_description
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Check if the response has an 'id' field
    if "id" in data and data["id"] is not None:
        return data["id"]
    
    # Return None for successful empty response or missing id
    return None