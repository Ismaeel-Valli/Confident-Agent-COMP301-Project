import requests

def solve(inputs):
    """
    Update selected fields of a post on DummyJSON.
    
    Inputs:
        - resource_id: Identifier of the post
        - new_body: value for the body attribute
        - new_title: value for the title attribute
    
    Returns:
        - The response's title value, or None if that attribute is absent.
        - None for a successful empty response.
        - Raises an exception for an unsuccessful HTTP response.
    """
    base_url = "https://dummyjson.com/posts"
    
    # Prepare the payload with only the fields to update
    payload = {
        "id": inputs["resource_id"],
        "title": inputs["new_title"],
        "body": inputs["new_body"]
    }
    
    try:
        response = requests.patch(f"{base_url}/{inputs['resource_id']}", json=payload)
        
        # Raise an exception for unsuccessful HTTP responses (status code not in 2xx range)
        if not response.ok:
            raise Exception(f"HTTP error occurred: {response.status_code} - {response.text}")
        
        # Return the title value from the response, or None if absent
        data = response.json()
        return data.get("title")
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Request failed: {e}")