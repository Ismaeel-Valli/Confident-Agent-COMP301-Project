import requests
import json

def solve(inputs):
    """
    Search REST Countries v5 using a search term.
    
    Args:
        inputs (dict): Dictionary containing:
            - search_text (str): The search term to use.
            - credential (str): Caller-supplied credential for authentication.
    
    Returns:
        dict or None: Decoded JSON response, or None if the response is empty.
    
    Raises:
        Exception: If the HTTP response is unsuccessful.
    """
    base_url = "https://api.restcountries.com"
    search_text = inputs["search_text"]
    credential = inputs["credential"]
    
    # Construct the API endpoint with the search term
    url = f"{base_url}/v5/search?name={search_text}"
    
    # Prepare headers with the credential
    headers = {
        "Authorization": f"Bearer {credential}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses
        
        data = response.json()
        
        # Return None if the response is empty (successful but no results)
        if not data:
            return None
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to decode JSON response: {e}")