def solve(inputs):
    import requests
    
    resource_id = inputs["resource_id"]
    new_albumId = inputs["new_albumId"]
    new_thumbnailUrl = inputs["new_thumbnailUrl"]
    new_title = inputs["new_title"]
    new_url = inputs["new_url"]
    
    url = f"https://jsonplaceholder.typicode.com/photos/{resource_id}"
    payload = {
        "albumId": new_albumId,
        "thumbnailUrl": new_thumbnailUrl,
        "title": new_title,
        "url": new_url
    }
    
    response = requests.put(url, json=payload)
    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    
    data = response.json()
    return data.get("title")