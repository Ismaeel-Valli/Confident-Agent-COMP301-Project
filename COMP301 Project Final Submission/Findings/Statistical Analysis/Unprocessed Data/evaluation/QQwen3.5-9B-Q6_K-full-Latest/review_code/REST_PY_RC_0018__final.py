import requests
import json

def solve(inputs):
    """
    Search country names using REST Countries v5 API.
    
    Args:
        inputs (dict): Contains:
            - excluded_attributes (list): Attributes to exclude from results
            - search_text (str): Search term for country names
            - credential (str): Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    api_url = "https://api.restcountries.com/v5.0/search"
    
    # Build query parameters
    params = {
        'search': inputs['search_text']
    }
    
    # Include credential in headers as per REST Countries v5 requirements
    headers = {
        'Authorization': f'Bearer {inputs["credential"]}'
    }
    
    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        
        # Filter out excluded attributes if any
        if inputs['excluded_attributes']:
            filtered_data = []
            for country in data:
                filtered_country = {}
                for key, value in country.items():
                    if key not in inputs['excluded_attributes']:
                        filtered_country[key] = value
                filtered_data.append(filtered_country)
            return filtered_data
        
        return data
    
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")