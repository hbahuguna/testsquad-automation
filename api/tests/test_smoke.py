import pytest
import httpx

@pytest.mark.asyncio
async def test_smoke_backend_health():
    # This will fail because the client pattern and logic aren't implemented yet
    from api.client.testsquad_client import TestSquadClient
    client = TestSquadClient(base_url="http://localhost:8000")
    status = await client.get_health()
    assert status == 200
