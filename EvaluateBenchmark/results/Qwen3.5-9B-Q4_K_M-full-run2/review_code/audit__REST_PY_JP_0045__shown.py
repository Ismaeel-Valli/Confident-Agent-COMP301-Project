def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_body = inputs["new_body"]
    new_email = inputs["new_email"]
    new_name = inputs["new_name"]
    new_post_identifier = inputs["new_post_identifier"]
    
    url = f"https://jsonplaceholder.typicode.com/comments/{resource_id}"
    payload = {
        "email": new_email,
        "name": new_name,
        "body": new_body,
        "postId": new_post_identifier
    }
    
    response = requests.put(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    return response.json().get("id")