import requests

def solve(inputs):
    included_fields = inputs.get("included_fields", "")
    base_url = "https://dummyjson.com"
    
    url = f"{base_url}/posts?page=1&limit=10"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("posts"):
            return None
        
        included_fields_set = set(f.strip() for f in included_fields.split(","))
        
        filtered_posts = []
        for post in data["posts"]:
            filtered_post = {}
            for key, value in post.items():
                if key in included_fields_set:
                    filtered_post[key] = value
            filtered_posts.append(filtered_post)
        
        return {
            "posts": filtered_posts,
            "total": data.get("total", 0),
            "skip": data.get("skip", 0),
            "limit": data.get("limit", 10),
            "hasMore": data.get("hasMore", False)
        }
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error: {e}")