import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_title = inputs['new_title']
    
    url = f"https://jsonplaceholder.typicode.com/todos/{resource_id}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "title": new_title
    }
    
    response = requests.patch(url, json=data, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"HTTP Error: {response.status_code} - {response.text}")
    
    # Check if the response is empty (no content)
    if not response.content:
        return None
    
    # Parse the JSON response and extract the 'id' attribute
    try:
        response_json = response.json()
        id_value = response_json.get('id')
        
        # If 'id' is absent in the response, return None
        if id_value is None:
            return None
        
        return id_value
    except ValueError:
        # In case the response is not valid JSON
        return None