import requests

def solve(inputs):
    """
    Submit a new album to JSONPlaceholder using the provided title.
    
    Args:
        inputs (dict): Must contain 'new_title' key with the album title string.
        
    Returns:
        int or None: The ID of the created album, or None if response is empty.
        
    Raises:
        requests.exceptions.RequestException: For unsuccessful HTTP responses.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/albums"  # Note: This endpoint does not exist in JSONPlaceholder
    
    title = inputs["new_title"]
    
    payload = {
        "title": title
    }
    
    try:
        response = requests.post(base_url + endpoint, json=payload)
        response.raise_for_status()
        
        if response.status_code == 201 or response.status_code == 200:
            data = response.json()
            return data.get("id")
        else:
            raise Exception(f"Unexpected status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        raise e