import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    
    url = "https://jsonplaceholder.typicode.com/todos/1"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'title': new_title
    }
    
    response = requests.patch(url, json=data, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
    
    if response.json():
        return response.json().get('id')
    else:
        return None