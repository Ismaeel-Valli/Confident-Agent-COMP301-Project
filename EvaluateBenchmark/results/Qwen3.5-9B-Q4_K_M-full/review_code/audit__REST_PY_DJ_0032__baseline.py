import requests

def solve(inputs):
    resource_id = inputs.get("resource_id")
    
    url = f"https://dummyjson.com/users/{resource_id}"
    response = requests.delete(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Check for 'id' in the response
    if "id" in data:
        return data["id"]
    
    # If successful but no 'id' (empty response), return None
    return None