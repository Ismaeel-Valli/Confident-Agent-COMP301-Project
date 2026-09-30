def solve(inputs):
    import requests
    
    base_url = "https://jsonplaceholder.typicode.com"
    
    # Construct the URL for comments endpoint with post_id from inputs
    post_id = inputs.get("post_id")
    url = f"{base_url}/comments?postId={post_id}"
    
    # Submit a new comment
    response = requests.post(url, json={
        "email": inputs["new_email"],
        "name": inputs["new_name"]
    })
    
    # Raise an exception for unsuccessful HTTP response
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    # Return the name value from the response, or None if absent
    data = response.json()
    return data.get("name")