```python
import requests

def solve(inputs):
    """
    Replaces a post record on JSONPlaceholder with the supplied data.
    
    Inputs:
        inputs['resource_id']: Identifier of the post (integer).
        inputs['new_body']: New value for the body attribute (string).
        inputs['new_title']: New value for the title attribute (string).
        inputs['new_user_identifier']: New value for the userId attribute (integer).
    
    Returns:
        The decoded JSON response if successful.
        None for a successful empty response.
    
    Raises:
        Exception for an unsuccessful HTTP response.
    """
    resource_id = inputs['resource_id']
    new_body = inputs['new_body']
    new_title = inputs['new_title']
    new_user_identifier = inputs['new_user_identifier']

    url = f"https://jsonplaceholder.typicode.com/posts/{resource_id}"
    payload = {
        "body": new_body,
        "title": new_title,
        "userId": new_user_identifier
    }

    response = requests.put(url, json=payload)
    
    if response.status_code == 200:
        return None
    else:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
```