import requests

def solve(inputs):
    """
    Replace a todo record in JSONPlaceholder with supplied data.
    
    Inputs:
        - resource_id: ID of the todo to update
        - new_completed: value for completed attribute
        - new_title: value for title attribute
        - new_user_identifier: value for user Id attribute
    
    Returns:
        - The response's 'title' value if present, otherwise None.
        - None for a successful empty response.
    
    Raises:
        Exception for unsuccessful HTTP responses.
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
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Return title if present, else None
    return data.get("title")