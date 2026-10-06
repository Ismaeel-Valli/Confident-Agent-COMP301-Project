import requests

def solve(inputs):
    """
    Replace a todo record with the supplied data.
    
    Args:
        inputs (dict): Contains:
            - resource_id: Identifier of the todo (int)
            - new_completed: value for the completed attribute (bool)
            - new_title: value for the title attribute (str)
            - new_user_identifier: value for the user Id attribute (int)
    
    Returns:
        int or None: The response's id value, or None if absent.
                     Returns None for a successful empty response.
    
    Raises:
        Exception: For an unsuccessful HTTP response.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/todos/{inputs['resource_id']}"
    
    payload = {
        "completed": inputs["new_completed"],
        "title": inputs["new_title"],
        "userId": inputs["new_user_identifier"]
    }
    
    response = requests.put(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    if data is None or len(data) == 0:
        return None
    
    return data.get("id")