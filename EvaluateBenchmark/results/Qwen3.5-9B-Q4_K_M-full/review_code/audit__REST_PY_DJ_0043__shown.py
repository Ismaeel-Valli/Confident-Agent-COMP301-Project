import requests

def solve(inputs):
    base_url = "https://dummyjson.com"
    
    # Create a new todo with the provided attributes using the correct endpoint
    payload = {
        "todo": inputs["new_todo"],
        "completed": inputs["new_completed"],
        "userId": inputs["new_user_identifier"]
    }
    
    response = requests.post(f"{base_url}/todos/add", json=payload)
    
    if response.status_code != 201:
        raise Exception(f"Failed to create todo: {response.status_code}")
    
    result = response.json()
    
    # Return the id of the created todo, or None if absent
    return result.get("id")