import requests

def solve(inputs):
    resource_id = inputs.get("resource_id")
    
    url = f"https://dummyjson.com/users/{resource_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Check for empty response (e.g., no users found or empty list)
    if not data.get("users"):
        return None
    
    user = data["users"][0]
    
    # Return the id value, or None if absent
    return user.get("id")