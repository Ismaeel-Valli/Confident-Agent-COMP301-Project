### Confidence Agent Report

**Decision:** deliver_with_flag
**EWCS:** 0.725 (signed: 0.725, applicable weight: 12)

| Layer | State | Tier | Weight | Factor | Positive | Signed |
|---|---|---|---|---|---|---|
| interface | verified_correct | tier_2 | 3 | 0.8 | 2.4 | 2.4 |
| identifier | verified_correct | tier_4 | 3 | 0.5 | 1.5 | 1.5 |
| access_point | verified_correct | tier_2 | 4 | 0.8 | 3.2 | 3.2 |
| input_contract | verified_correct | tier_2 | 2 | 0.8 | 1.6 | 1.6 |
| output_contract | not_applicable | none | 1 | 0 | 0 | 0 |
| contextual | not_applicable | none | 2 | 0 | 0 | 0 |

Scope: API-claim and static evidence only. EWCS is not a probability of correctness. Task behavior has not been independently checked by this verifier.

Policy 2026-09-25.1: thresholds 0.85/0.6, uncertainty gate on.

Evidence:

- interface: requests maps to requests (2.34.2). Installation/callables checked separately by Pyright.
- identifier: No identifier, attribute or API-call diagnostics in the configured environment (Pyright standard mode). A clean check does not establish REST contracts or task behavior.
- access_point: GET https://jsonplaceholder.typicode.com/posts matches the declared server and operation GET /posts.
- input_contract: Required inputs, locations and supported value constraints checked for call_21_19 (/posts).
- output_contract: No tracked response-field accesses.
- contextual: No authentication requirement for this operation. Unused security definitions are not requirements.

Flag: some checks rely on supporting static or package metadata evidence; the code was not executed.

```python
import requests

def solve(inputs):
    """
    Retrieve posts from JSONPlaceholder and return the decoded JSON response.
    
    Parameters:
        inputs (dict): Must contain 'post_id' key with an integer value.
    
    Returns:
        dict or None: Decoded JSON response, or None if successful but empty.
    
    Raises:
        Exception: If HTTP response is unsuccessful.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    endpoint = "/posts"
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        if response.status_code == 200 and len(response.json()) == 0:
            return None
        
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error occurred: {e}")
```