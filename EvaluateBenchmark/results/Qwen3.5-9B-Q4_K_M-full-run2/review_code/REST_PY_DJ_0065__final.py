import requests

def solve(inputs):
    included_fields = inputs.get("included_fields", "")
    base_url = "https://dummyjson.com/users"
    
    params = {"limit": 1}
    if included_fields:
        fields_list = [f.strip() for f in included_fields.split(",")]
        params["fields"] = ",".join(fields_list)
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    data = response.json()
    
    if not data.get("users"):
        return None
    
    return data["users"]