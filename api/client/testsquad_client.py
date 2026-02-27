import httpx

class TestSquadClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get_health(self) -> int:
        # Correct endpoint found in app.py
        response = await self.client.get("/api/health")
        return response.status_code

    async def close(self):
        await self.client.aclose()
