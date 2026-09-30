import requests

def solve(inputs):
    """
    Replace a photo record in JSONPlaceholder with the supplied data.
    
    Inputs:
        inputs['resource_id']: Identifier of the photo (int)
        inputs['new_albumId']: New value for albumId attribute (int or None)
        inputs['new_thumbnailUrl']: New value for thumbnailUrl attribute (str or None)
        inputs['new_title']: New value for title attribute (str or None)
        inputs['new_url']: New value for url attribute (str or None)
    
    Returns:
        The response's id value (int), or None if that attribute is absent.
        Returns None for a successful empty response.
    
    Raises:
        Exception for an unsuccessful HTTP response.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    resource_id = inputs['resource_id']
    
    payload = {
        'albumId': inputs.get('new_albumId'),
        'id': resource_id,  # Keep the original id for PUT to work on specific resource
        'thumbnailUrl': inputs.get('new_thumbnailUrl'),
        'title': inputs.get('new_title'),
        'url': inputs.get('new_url')
    }
    
    response = requests.put(f"{base_url}/photos/{resource_id}", json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    # Return the id from response, or None if absent
    return data.get('id')