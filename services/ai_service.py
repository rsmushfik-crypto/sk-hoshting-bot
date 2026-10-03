from config import settings


async def ask_ai(
    message: str
):

    if not settings.OPENAI_API_KEY:

        return (
            "OPENAI_API_KEY সেট করা হয়নি।"
        )

    # এখানে আপনার AI provider
    # SDK/API call থাকবে।

    return "AI response"
