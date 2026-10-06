import requests

def solve(inputs):
    new_title = inputs['new_title']
    
    try:
        response = requests.post(
            'https://jsonplaceholder.typicode.com/todos',
            json={'title': new_title}
        )
        
        if response.status_code != 201 and response.status_code != 200:
            raise Exception(f"Failed to create todo. Status code: {response.status_code}")
            
        data = response.json()
        
        if not data:
            return None
            
        return data.get('title')
        
    except requests.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")