from fastapi import APIRouter

from database import (
    SessionLocal,
    User
)

from schemas import UserRequest


router = APIRouter()


@router.post("/")
def create_user(
    request: UserRequest
):

    db = SessionLocal()

    try:

        user = db.query(User).filter(
            User.telegram_id
            == request.telegram_id
        ).first()

        if not user:

            user = User(
                telegram_id=request.telegram_id,
                username=request.username,
                first_name=request.first_name
            )

            db.add(user)

        db.commit()

        return {
            "success": True
        }

    finally:

        db.close()
