import pytest
import httpx
import time

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_trigger_scan_and_poll():
    """
    Validates that the /api/scan endpoint correctly triggers an asynchronous
    Agent engine execution, and that the /api/scan/{scan_id} endpoint can be 
    polled for its status updates.
    """
    # 1. Trigger the scan
    payload = {"path": "/tmp/dummy/project/path"}
    
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/api/scan", json=payload)
        
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert "scan_id" in data
    assert data["status"] == "pending"
    
    scan_id = data["scan_id"]
    
    # 2. Poll the scan status until it completes or fails
    max_retries = 30
    retry_interval = 0.5
    
    final_status = None
    
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        for _ in range(max_retries):
            poll_resp = await client.get(f"/api/scan/{scan_id}")
            assert poll_resp.status_code == 200
            
            poll_data = poll_resp.json()
            status = poll_data.get("status")
            
            if status in ["completed", "failed"]:
                final_status = status
                break
                
            time.sleep(retry_interval)
            
    # We just want to assert the backend infrastructure handles the state transition.
    # In a fully bootstrapped MOCK_LLM environment, it should eventually transition.
    assert final_status is not None, "Scan timed out before reaching a terminal state"
    
