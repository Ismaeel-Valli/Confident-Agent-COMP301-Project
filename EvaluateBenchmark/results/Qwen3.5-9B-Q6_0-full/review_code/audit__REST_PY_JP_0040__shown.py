import requests


def solve(inputs):
    """Replace a post record in JSONPlaceholder with supplied data."""
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/posts/{inputs['resource_id']}"
    
    payload = {
        "body": inputs["new_body"],
        "title": inputs["new_title"],
        "userId": inputs["new_user_identifier"]
    }
    
    try:
        response = requests.put(url, json=payload)
        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            return data.get("id")
        else:
            return None
            
    except requests.exceptions.HTTPError as e:
        raise e