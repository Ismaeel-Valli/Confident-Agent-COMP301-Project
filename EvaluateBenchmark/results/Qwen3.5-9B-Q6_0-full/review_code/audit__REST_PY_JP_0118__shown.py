import requests

def solve(inputs):
    """
    Submit a new album to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): Must contain 'new_title' and 'new_user_identifier'.
        
    Returns:
        str or None: The title from the response, or None if absent or empty response.
        
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/albums"
    
    payload = {
        "title": inputs["new_title"],
        "userId": inputs["new_user_identifier"]
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        if response.status_code == 201:
            data = response.json()
            return data.get("title")
        else:
            raise Exception(f"Unexpected status code: {response.status_code}")
            
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")