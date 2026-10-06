import requests

def solve(inputs):
    """
    Look up countries by exact match on their capital city using REST Countries v5.
    
    Args:
        inputs (dict): {
            "value": str - The capital city to match exactly,
            "excluded_attributes": list[str] - Attributes to exclude from results,
            "credential": str - Caller-supplied credential with necessary permissions
        }
    
    Returns:
        dict or None - Decoded JSON response (None for successful empty response)
    
    Raises:
        Exception - For unsuccessful HTTP responses
    """
    base_url = "https://api.restcountries.com"
    url = f"{base_url}/v5/capital/{inputs['value']}"
    
    headers = {
        "Authorization": f"Bearer {inputs['credential']}",
        "Accept": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    # Filter out excluded attributes if any
    if inputs["excluded_attributes"]:
        filtered_data = []
        for country in data:
            filtered_country = {k: v for k, v in country.items() 
                              if k not in inputs["excluded_attributes"]}
            filtered_data.append(filtered_country)
        return filtered_data
    
    return data