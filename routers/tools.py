from fastapi import APIRouter

from tools.registry import (
    TOOLS,
    get_categories
)

router = APIRouter()


@router.get("/")
def all_tools():

    return TOOLS


@router.get("/categories")
def categories():

    return get_categories()


@router.get("/{slug}")
def tool(slug: str):

    from tools.registry import get_tool

    result = get_tool(slug)

    if not result:

        return {
            "error": "Tool not found"
        }

    return result
