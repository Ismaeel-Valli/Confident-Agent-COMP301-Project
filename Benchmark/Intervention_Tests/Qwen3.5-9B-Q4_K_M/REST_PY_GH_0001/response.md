### Confidence Agent Report

**Decision:** deliver_with_flag
**EWCS:** 0.825 (signed: 0.825, applicable weight: 12)

| Layer | State | Tier | Weight | Factor | Positive | Signed |
|---|---|---|---|---|---|---|
| interface | verified_correct | tier_2 | 3 | 0.8 | 2.4 | 2.4 |
| identifier | verified_correct | tier_4 | 3 | 0.5 | 1.5 | 1.5 |
| access_point | verified_correct | tier_1 | 4 | 1 | 4 | 4 |
| input_contract | verified_correct | tier_1 | 2 | 1 | 2 | 2 |
| output_contract | not_applicable | none | 1 | 0 | 0 | 0 |
| contextual | not_applicable | none | 2 | 0 | 0 | 0 |

Scope: API-claim and static evidence only. EWCS is not a probability of correctness. Task behavior has not been independently checked by this verifier.

Policy 2026-09-25.1: thresholds 0.85/0.6, uncertainty gate on.

Evidence:

- interface: requests maps to requests (2.34.2). Installation/callables checked separately by Pyright. json is in the verification interpreter's standard library (sys.stdlib_module_names).
- identifier: No identifier, attribute or API-call diagnostics in the configured environment (Pyright standard mode). A clean check does not establish REST contracts or task behavior.
- access_point: GET https://api.github.com/orgs/{org} matches the declared server and operation GET /orgs/{org}. Noncritical: runtime path values are assumed to stay within one path segment.
- input_contract: Required inputs, locations and supported value constraints checked for call_29_15 (/orgs/{org}). Noncritical: path.org: runtime value org is not statically known; its value constraints are not checked; Undeclared header x-github-api-version; acceptance is undocumented
- output_contract: No tracked response-field accesses.
- contextual: No authentication requirement for this operation. Unused security definitions are not requirements.

Flag: some checks rely on supporting static or package metadata evidence; the code was not executed.

```python
import requests
import json

def solve(inputs):
    """
    Get an organization from GitHub REST API version 2026-03-10.
    
    Args:
        inputs (dict): Dictionary containing:
            - organization (str): The organization name.
            - credential (str): Caller-supplied authentication token.
    
    Returns:
        dict or None: Decoded JSON response, or None for successful empty response.
    
    Raises:
        Exception: For unsuccessful HTTP responses.
    """
    org_name = inputs["organization"]
    auth_token = inputs["credential"]
    
    url = "https://api.github.com/orgs/{org}".format(org=org_name)
    headers = {
        "Authorization": f"token {auth_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 204:
        return None
    else:
        raise Exception(f"Failed to fetch organization {org_name}: HTTP {response.status_code}")
```