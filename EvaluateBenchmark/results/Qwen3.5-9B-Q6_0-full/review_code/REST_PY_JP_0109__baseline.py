import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_url = inputs['new_url']
    
    url = "https://jsonplaceholder.typicode.com/photos/1"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "id": resource_id,
        "url": new_url
    }

    try:
        response = requests.patch(url, json=data, headers=headers)
        response.raise_for_status()
        
        if response.status_code == 204:
            return None
        
        data_response = response.json()
        return data_response.get('id')
    
    except requests.exceptions.HTTPError as errh:
        raise Exception(f"HTTP Error occurred: {errh}")
    except requests.exceptions.RequestException as err:
        raise Exception(f"Request failed: {err}")