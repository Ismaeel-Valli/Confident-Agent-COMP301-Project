import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_thumbnailUrl = inputs['new_thumbnailUrl']
    
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "thumbnailUrl": new_thumbnailUrl
    }
    
    response = requests.patch(url, json=data, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP request failed with status code: {response.status_code}")
    
    if response.text.strip() == "":
        return None
    
    try:
        data_dict = response.json()
        return data_dict.get('id')
    except ValueError:
        return None