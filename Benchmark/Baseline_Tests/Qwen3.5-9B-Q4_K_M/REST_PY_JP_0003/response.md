```python
import requests

def solve(inputs):
    """
    Retrieves a post by identifier from JSONPlaceholder.
    
    Args:
        inputs (dict): A dictionary containing 'resource_id' as the post identifier.
        
    Returns:
        dict or None: The decoded JSON response if successful and not empty, 
                      None if the response is successfully empty.
                      
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    resource_id = inputs['resource_id']
    url = f"https://jsonplaceholder.typicode.com/posts/{resource_id}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # JSONPlaceholder doesn't typically return empty responses for valid post IDs,
    # but per instructions, we return None for a successful empty response.
    if not data:
        return None
        
    return data
```