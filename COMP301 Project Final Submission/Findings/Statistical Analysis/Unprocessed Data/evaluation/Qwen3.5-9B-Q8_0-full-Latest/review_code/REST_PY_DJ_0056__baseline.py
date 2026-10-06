import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    
    url = f"https://dummyjson.com/posts/{resource_id}"
    response = requests.delete(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to delete post: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Check for successful empty response (no content or specific success structure)
    if not data.get('content'):
        return None
    
    # Return title if present, otherwise None
    return data.get('title')