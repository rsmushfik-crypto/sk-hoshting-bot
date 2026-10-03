async def translate(
    text: str,
    target_language: str
):

    # Translation API এখানে connect হবে।

    return {
        "text": text,
        "target": target_language
    }
