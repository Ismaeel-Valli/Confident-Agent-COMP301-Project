import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    new_user_identifier = inputs['new_user_identifier']
    
    url = "https://jsonplaceholder.typicode.com/albums"
    payload = {
        'id': resource_id,
        'title': new_title,
        'userId': new_user_identifier
    }
    
    try:
        response = requests.put(url, json=payload)
        response.raise_for_status()
        
        if response.status_code == 204:
            return None
        
        data = response.json()
        return data.get('title')
    
    except requests.exceptions.HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        raise Exception(f"Request error occurred: {req_err}")