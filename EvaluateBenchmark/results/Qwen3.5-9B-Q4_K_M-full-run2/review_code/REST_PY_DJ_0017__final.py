import requests

def solve(inputs):
    search_text = inputs["search_text"]
    base_url = "https://dummyjson.com/posts"
    url = f"{base_url}?search={search_text}"
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    if data["posts"]:
        return data["posts"]
    else:
        return None