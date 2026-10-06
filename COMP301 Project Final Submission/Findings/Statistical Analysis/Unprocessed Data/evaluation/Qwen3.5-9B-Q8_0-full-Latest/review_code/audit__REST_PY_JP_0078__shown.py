import requests

def solve(inputs):
    """Submit a new photo to JSONPlaceholder and return its title."""
    base_url = "https://jsonplaceholder.typicode.com"
    url = f"{base_url}/photos"
    
    try:
        response = requests.post(url, json={"title": inputs["new_title"]})
        
        if response.status_code != 200:
            raise Exception(f"Failed to submit photo. HTTP {response.status_code}: {response.text}")
        
        data = response.json()
        
        # Return title if present, otherwise None for successful empty response
        return data.get("title")
    except requests.RequestException as e:
        raise Exception(f"Request failed: {e}")