def solve(inputs):
    import requests
    
    search_text = inputs["search_text"]
    results_to_skip = inputs["results_to_skip"]
    credential = inputs["credential"]
    
    base_url = "https://api.restcountries.com/v5.0/search"
    params = {
        "name": search_text,
        "skip": results_to_skip
    }
    
    headers = {
        "Authorization": f"Bearer {credential}"
    }
    
    response = requests.get(base_url, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    if len(data) == 0:
        return None
    
    return data