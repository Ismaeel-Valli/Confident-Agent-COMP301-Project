import requests

def solve(inputs):
    """
    Look up countries by exact match on their bordering country code using REST Countries v5.
    
    Args:
        inputs (dict): Contains:
            - "value": The country code to match exactly against borders
            - "included_attributes": List of attributes to include in response
            - "credential": Caller-supplied credential
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response
    
    Raises:
        Exception: For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com/v5.0"
    
    # Build the URL with the border country code parameter
    url = f"{base_url}/borders/{inputs['value']}"
    
    # Prepare headers with credential
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"HTTP error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        # If included_attributes is specified, filter the response
        if inputs.get("included_attributes"):
            if isinstance(data, dict):
                filtered_data = {key: value for key, value in data.items() 
                               if key in inputs["included_attributes"]}
                return filtered_data
            elif isinstance(data, list):
                filtered_data = []
                for item in data:
                    if isinstance(item, dict):
                        filtered_item = {key: value for key, value in item.items() 
                                       if key in inputs["included_attributes"]}
                        filtered_data.append(filtered_item)
                    else:
                        filtered_data.append(item)
                return filtered_data
        
        return data
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {str(e)}")