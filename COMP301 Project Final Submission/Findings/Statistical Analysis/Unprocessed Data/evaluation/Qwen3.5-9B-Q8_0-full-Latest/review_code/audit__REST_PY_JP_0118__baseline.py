import requests

def solve(inputs):
    """
    Submits a new album to JSONPlaceholder using the provided inputs.
    
    Args:
        inputs (dict): A dictionary containing:
            - 'new_title': The title for the new album.
            - 'new_user_identifier': The user ID for the new album.
    
    Returns:
        str or None: The title of the created album if present in the response, 
                     otherwise None for a successful empty response.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = f"{base_url}/albums"
    
    payload = {
        "title": inputs['new_title'],
        "userId": inputs['new_user_identifier']
    }
    
    try:
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        
        if response.status_code == 201:
            data = response.json()
            return data.get('title')
        elif response.status_code == 204:
            return None
        else:
            # This case should ideally not be reached due to raise_for_status(), 
            # but kept for explicit handling of non-201/204 success codes if any.
            raise Exception(f"Unexpected successful status code: {response.status_code}")
            
    except requests.exceptions.HTTPError as e:
        raise e
    except requests.exceptions.RequestException as e:
        raise e