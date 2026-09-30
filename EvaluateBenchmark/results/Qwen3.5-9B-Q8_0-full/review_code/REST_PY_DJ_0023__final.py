import requests

def solve(inputs):
    """
    Submit a new todo to DummyJSON API.
    
    Args:
        inputs (dict): Contains:
            - new_completed (bool): Value for the 'completed' attribute
            - new_todo (str): Value for the 'title' attribute
            - new_user_identifier (int): Value for the 'userId' attribute
    
    Returns:
        dict or None: Decoded JSON response, or None if successful empty response
    """
    base_url = "https://dummyjson.com/todos/add"
    
    payload = {
        "title": inputs["new_todo"],
        "completed": inputs["new_completed"],
        "userId": inputs["new_user_identifier"]
    }
    
    try:
        response = requests.post(base_url, json=payload)
        response.raise_for_status()
        
        if response.status_code == 201 or response.status_code == 200:
            data = response.json()
            # DummyJSON returns the created todo in the response body for POST
            return data if data else None
        else:
            raise Exception(f"HTTP error {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")