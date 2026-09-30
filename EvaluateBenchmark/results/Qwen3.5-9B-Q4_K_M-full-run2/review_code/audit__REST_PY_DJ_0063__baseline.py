import requests

def solve(inputs):
    resource_id = inputs.get('resource_id')
    
    # Assuming a base URL; adjust as needed for DummyJSON or your specific setup
    url = f"https://dummyjson.com/products/{resource_id}"
    
    try:
        response = requests.delete(url)
        
        if response.status_code != 200:
            raise Exception(f"Unsuccessful HTTP response: {response.status_code}")
        
        # Check for 'isDeleted' attribute in the response JSON
        data = response.json()
        
        if 'isDeleted' in data:
            return data['isDeleted']
        else:
            # Return None for a successful empty response or if isDeleted is absent
            return None
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")