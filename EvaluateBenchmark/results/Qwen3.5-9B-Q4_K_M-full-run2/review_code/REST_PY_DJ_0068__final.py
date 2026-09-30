def solve(inputs):
    """Retrieve one page of posts from DummyJSON."""
    import requests
    
    included_fields = inputs.get("included_fields", "")
    base_url = "https://dummyjson.com"
    
    url = f"{base_url}/posts?page=1&limit=10"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"HTTP error {response.status_code}: {response.text}")
    
    data = response.json()
    
    if not data.get("posts"):
        return None
    
    selected_fields = included_fields.split(",") if included_fields else []
    
    filtered_posts = []
    for post in data["posts"]:
        filtered_post = {}
        for field in selected_fields:
            field = field.strip()
            if field in post:
                filtered_post[field] = post[field]
        filtered_posts.append(filtered_post)
    
    return filtered_posts