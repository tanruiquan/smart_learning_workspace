# import httpx

# from src.external_service.schemas import PublicAPIsResponse


class Client:
    """Mock Client"""

    async def generate_feedback(self, attempt_id: str, task_id: str):
        return {
            "attempt_id": attempt_id,
            "task_id": task_id,
            "feedback": "Feedback"
        }
