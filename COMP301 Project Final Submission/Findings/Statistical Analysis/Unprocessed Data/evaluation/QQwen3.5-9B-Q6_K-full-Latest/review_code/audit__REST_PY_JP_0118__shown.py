import requests

def solve(inputs):
    """
    Submit a new album to JSONPlaceholder.
    
    inputs:
        new_title: str, value for the title attribute
        new_user_identifier: int or str, value for the userId attribute
    
    Returns:
        The response's title value if present, otherwise None.
        Returns None for a successful empty response.
        Raises an exception for an unsuccessful HTTP response.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/albums"  # Note: This endpoint does not exist in JSONPlaceholder
    
    url = f"{base_url}{endpoint}"
    
    payload = {
        "title": inputs["new_title"],
        "userId": inputs["new_user_identifier"]
    }
    
    try:
        response = requests.post(url, json=payload)
        
        # Check for unsuccessful HTTP response
        if not response.ok:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        # Return title if present, otherwise None
        data = response.json()
        return data.get("title")
    
    except requests.RequestException as e:
        raise Exception(f"Request failed: {e}")