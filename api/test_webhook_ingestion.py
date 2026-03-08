import pytest
import httpx
import hmac
import hashlib
import json
import os

from typing import Dict, Any

# Assuming backend runs on 8000
BASE_URL = "http://localhost:8000"

# Derived from webhooks.py: fallback secret for dev environment
WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET", "your_development_webhook_secret").encode()

def generate_github_signature(payload_bytes: bytes) -> str:
    """Generates the X-Hub-Signature-256 header as expected by the backend."""
    digest = hmac.new(WEBHOOK_SECRET, payload_bytes, hashlib.sha256).hexdigest()
    return f"sha256={digest}"

@pytest.mark.asyncio
async def test_webhook_ingestion_success():
    """
    Validates that the /webhooks/github endpoint correctly processes a simulated 
    PR 'opened' event, validating signatures and accepting the payload.
    """
    payload_dict: Dict[str, Any] = {
        "action": "opened",
        "pull_request": {
            "number": 999
        },
        "repository": {
            "full_name": "hbahuguna/e2e-dummy-repo"
        }
    }
    
    payload_bytes = json.dumps(payload_dict).encode("utf-8")
    signature = generate_github_signature(payload_bytes)

    headers = {
        "X-GitHub-Event": "pull_request",
        "X-Hub-Signature-256": signature,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/webhooks/github", content=payload_bytes, headers=headers)
        
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("status") == "processed", "Webhook was not processed correctly"

@pytest.mark.asyncio
async def test_webhook_ingestion_invalid_signature():
    """
    Validates that the webhook endpoint rejects payloads with invalid signatures.
    """
    payload_dict: Dict[str, Any] = {
        "action": "opened",
        "pull_request": {"number": 1},
        "repository": {"full_name": "test/repo"}
    }
    
    payload_bytes = json.dumps(payload_dict).encode("utf-8")
    
    headers = {
        "X-GitHub-Event": "pull_request",
        "X-Hub-Signature-256": "sha256=invalid_signature_hash_here",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/webhooks/github", content=payload_bytes, headers=headers)
        
    assert response.status_code == 401
    assert response.json().get("detail") == "Invalid signature"
