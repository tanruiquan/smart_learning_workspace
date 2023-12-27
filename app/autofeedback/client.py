# import httpx

# from src.external_service.schemas import PublicAPIsResponse


# class Client:
#     """
#     This is the client to Public APIs service,
#     which returns the list of APIs with public access.
#     """

#     BASE_URL: str = "https://api.publicapis.org"

#     @property
#     def client(self):
#         return httpx.AsyncClient(base_url=self.BASE_URL, timeout=10.0)

#     async def get_public_apis(self) -> PublicAPIsResponse:
#         async with self.client as client:
#             response = await client.get("/entries")

#             return PublicAPIsResponse.model_validate_json(response.read())
class Client:
    """Mock Client"""

    async def generate_feedback(self, attempt_id: str, task_id: str):
        return {
            "attempt_id": attempt_id,
            "task_id": task_id,
            "feedback": "Feedback"
        }
