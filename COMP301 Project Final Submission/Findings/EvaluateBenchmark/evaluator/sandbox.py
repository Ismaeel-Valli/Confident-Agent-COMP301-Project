"""Runs a candidate in a separate, isolated Python process (see sandbox_harness.py)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HARNESS = Path(__file__).resolve().parent.parent / "sandbox_harness.py"
MARKER = "@@RESULT@@"


def run(code: str, inputs: dict, scenario: str, response_shape: dict, success_status: int,
        timeout: float = 10.0, python: str | None = None) -> dict:
    """scenario: 'ok' (documented response), 'empty' (204, no body) or 'error' (500)."""
    job = {"code": code, "inputs": inputs, "scenario": scenario, "response_shape": response_shape,
           "success_status": success_status}
    # -I: isolated (no user site, environment variables ignored); -S: no site-packages, so the
    # only 'requests' the candidate can import is the recording stand-in.
    cmd = [python or sys.executable, "-I", "-S", str(HARNESS)]
    env = {k: v for k, v in os.environ.items() if k.upper() in ("SYSTEMROOT", "WINDIR", "TEMP", "TMP")}
    with tempfile.TemporaryDirectory(prefix="eval-sandbox-") as cwd:
        try:
            out = subprocess.run(cmd, input=json.dumps(job), capture_output=True, text=True, encoding="utf-8",
                                 timeout=timeout, cwd=cwd, env=env)
        except subprocess.TimeoutExpired:
            return {"exception": "Timeout", "message": f"did not finish within {timeout} s", "requests": [],
                    "reads": [], "library_errors": [], "unsupported": []}
    # The harness writes its result last; anything the candidate printed comes before it.
    for line in reversed(out.stdout.splitlines()):
        if line.startswith(MARKER):
            return json.loads(line[len(MARKER):])
    return {"exception": "SandboxCrash", "message": (out.stderr or out.stdout)[-500:], "requests": [], "reads": [],
            "library_errors": [], "unsupported": []}
