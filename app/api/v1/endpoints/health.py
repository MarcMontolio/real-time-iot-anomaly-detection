"""
Health check endpoint
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Basic health check endpoint.
    
    Returns a simple status indicator confirming that the API is live.
    """
    return {"status": "ok"}
    