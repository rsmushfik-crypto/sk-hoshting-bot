from pydantic import BaseModel


class ToolRequest(BaseModel):

    telegram_id: int

    tool: str

    text: str = ""


class UserRequest(BaseModel):

    telegram_id: int

    username: str = ""

    first_name: str = ""


class AIRequest(BaseModel):

    telegram_id: int

    message: str
