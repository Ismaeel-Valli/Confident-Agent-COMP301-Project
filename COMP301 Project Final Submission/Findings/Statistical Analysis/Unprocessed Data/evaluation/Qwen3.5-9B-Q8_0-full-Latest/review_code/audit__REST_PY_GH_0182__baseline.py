import requests
from typing import Dict, Any, Optional, List

def solve(inputs: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    """
    Fetches issue comments from a GitHub repository using the REST API version 2026-03-10.
    
    Args:
        inputs (dict): A dictionary containing:
            - repository_owner (str): The account owner of the repository.
            - repository_name (str): The name of the repository without the .git extension.
            - issue_number (int): The number that identifies the issue.
            - since (str, optional): ISO 8601 timestamp to filter comments updated after this time.
            - page_size (int, optional): Number of results per page (max 100).
            - credential (str): Bearer token for authentication.
    
    Returns:
        Optional[List[Dict[str, Any]]]: A list of decoded JSON responses for issue comments, 
                                       or None if the response is successfully empty.
    
    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
    """
    owner = inputs["repository_owner"]
    repo = inputs["repository_name"]
    issue_number = inputs["issue_number"]
    since = inputs.get("since")
    page_size = min(inputs.get("page_size", 30), 100)
    credential = inputs["credential"]
    
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"Bearer {credential}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    params = {}
    if since:
        params["since"] = since
    if page_size != 30:  # Only add if different from default
        params["per_page"] = page_size
    
    all_comments = []
    
    while True:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch issue comments. Status code: {response.status_code}, Response: {response.text}")
        
        data = response.json()
        
        if not data:
            return None
        
        all_comments.extend(data)
        
        # Check for pagination
        link_header = response.headers.get("Link", "")
        if "rel=\"next\"" not in link_header:
            break
        
        # Prepare next page parameters manually since we can't easily parse Link header without extra logic
        # For simplicity, we'll just increment a page counter and let GitHub handle it via per_page
        # However, the API doesn't use page numbers directly for this endpoint in the same way.
        # We rely on the fact that if 'next' is present, we need to fetch more.
        # Since we can't easily extract the next URL from the Link header without parsing,
        # and the problem states "Assume referenced resources and accounts exist", 
        # we'll assume a single page or that the user expects basic pagination handling.
        # A robust solution would parse the Link header, but for this constraint, 
        # we'll stop if no 'next' is found.
        
        # Note: The above loop condition checks for 'next', but we don't update params for the next page
        # because GitHub's pagination for this endpoint uses a cursor or just returns all available in one go 
        # if per_page is set high enough, OR it requires parsing the Link header to get the next URL.
        # Given the constraints and typical usage, let's assume we need to handle pagination properly.
        
        # Correct approach for GitHub pagination:
        # We need to parse the Link header to get the 'next' URL.
        # However, to keep it simple and within the scope of a basic function without external dependencies 
        # for parsing, and given the instruction "Do not execute the function", we will implement a basic version.
        # A full implementation would require regex or string manipulation on the Link header.
        
        # Let's break out if no next link is found to avoid infinite loops in this simplified version.
        # In a real-world scenario, you'd parse the Link header.
        break  # Breaking here because implementing full Link header parsing might be overkill for this snippet 
               # and the problem doesn't specify how many pages. We'll assume one page or that the user 
               # sets per_page high enough. If multiple pages are needed, a more complex parser is required.
               # But wait, the loop condition was `if "rel=\"next\"" not in link_header: break`. 
               # So if it IS present, we continue. But we don't update params for the next page.
               # This is a flaw in the initial thought process.
    
    # Re-evaluating pagination: GitHub's API uses Link header for pagination.
    # We need to extract the 'next' URL and make the next request with that URL.
    # Let's refactor slightly to handle this correctly within the loop.
    
    # Resetting all_comments and starting over with proper pagination logic
    all_comments = []
    current_url = url
    
    while True:
        response = requests.get(current_url, headers=headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch issue comments. Status code: {response.status_code}, Response: {response.text}")
        
        data = response.json()
        
        if not data:
            return None
        
        all_comments.extend(data)
        
        link_header = response.headers.get("Link", "")
        if "rel=\"next\"" not in link_header:
            break
        
        # Extract the next URL from the Link header
        import re
        match = re.search(r'<([^>]+)>;\s*rel="next"', link_header)
        if match:
            current_url = match.group(1)
        else:
            break
            
    return all_comments