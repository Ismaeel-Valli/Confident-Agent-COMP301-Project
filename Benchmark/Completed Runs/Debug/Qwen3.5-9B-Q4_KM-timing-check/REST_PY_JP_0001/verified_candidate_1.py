import requests

def solve(inputs):
    """
    Retrieve posts from JSONPlaceholder and return decoded JSON.
    
    - Returns None for a successful empty response.
    - Raises an exception for an unsuccessful HTTP response.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/posts"
    
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check for empty response
            if not data:
                return None
            
            return data
        else:
            raise Exception(f"HTTP {response.status_code}: Failed to retrieve posts")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")