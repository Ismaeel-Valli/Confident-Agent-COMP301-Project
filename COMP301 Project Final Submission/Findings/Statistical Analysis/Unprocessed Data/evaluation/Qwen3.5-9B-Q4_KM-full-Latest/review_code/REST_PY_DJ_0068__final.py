import requests

def solve(inputs):
    included_fields = inputs.get("included_fields", "")
    base_url = "https://dummyjson.com"
    
    if included_fields:
        fields_list = [f.strip() for f in included_fields.split(",")]
        params = {"include": ",".join(fields_list)}
    else:
        params = {}
    
    response = requests.get(f"{base_url}/posts", params=params)
    
    if response.status_code != 200:
        raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
    
    data = response.json()
    
    if not data.get("posts"):
        return None
    
    return data