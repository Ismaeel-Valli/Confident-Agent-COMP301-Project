```python
import requests

def solve(inputs):
    """
    Submits a new post to JSONPlaceholder using the provided inputs dictionary.
    
    Args:
        inputs (dict): A dictionary containing 'new_title' for the post title.
        
    Returns:
        dict or None: The decoded JSON response if successful, or None for an empty response.
        
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    
    # Prepare the payload with the new title and other required fields
    payload = {
        "title": inputs["new_title"],
        "body": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "userId": 1
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 201:
        # Return None for a successful empty response (though JSONPlaceholder typically returns the created object)
        return None if response.text.strip() == "" else response.json()
    elif response.status_code >= 400:
        raise Exception(f"Failed to submit post. HTTP Status Code: {response.status_code}, Response: {response.text}")
    
    # Handle other unexpected status codes
    raise Exception(f"Unexpected HTTP Status Code: {response.status_code}")
```