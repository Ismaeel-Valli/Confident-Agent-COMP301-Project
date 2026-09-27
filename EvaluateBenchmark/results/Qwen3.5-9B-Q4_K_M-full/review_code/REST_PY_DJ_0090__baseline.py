import requests

def solve(inputs):
    resource_id = inputs['resource_id']
    new_body = inputs['new_body']
    
    url = f"https://dummyjson.com/posts/{resource_id}"
    payload = {"body": new_body}
    
    response = requests.patch(url, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update post: {response.text}")
    
    result = response.json()
    
    if result.get('statusCode') == 200 and result.get('message'):
        return None
    
    title = result.get('title')
    return title