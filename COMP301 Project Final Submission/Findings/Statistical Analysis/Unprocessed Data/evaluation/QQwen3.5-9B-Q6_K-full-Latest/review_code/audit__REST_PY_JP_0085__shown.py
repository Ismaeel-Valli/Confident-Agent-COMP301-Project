import requests

def solve(inputs):
    """
    Update a todo in JSONPlaceholder with a new title.
    
    Args:
        inputs (dict): Dictionary containing:
            - resource_id (int): ID of the todo to update
            - new_title (str): New title value
    
    Returns:
        str or None: The updated todo's title, or None if absent/empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs["resource_id"]
    new_title = inputs["new_title"]
    
    url = f"{base_url}/todos/{resource_id}"
    
    try:
        response = requests.patch(url, json={"title": new_title})
        
        if response.status_code != 200:
            raise Exception(f"Failed to update todo. Status code: {response.status_code}")
        
        data = response.json()
        
        # Return title if present, otherwise None for successful empty response
        return data.get("title")
    
    except requests.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")