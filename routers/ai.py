from fastapi import APIRouter

from schemas import AIRequest

router = APIRouter()


@router.post("/chat")
async def chat(
    request: AIRequest
):

    return {
        "success": True,
        "message": (
            "AI service adapter এখানে "
            "connect করতে হবে।"
        ),
        "input": request.message
    }
