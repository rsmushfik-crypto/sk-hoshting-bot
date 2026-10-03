import httpx

from config import settings


async def weather(
    city: str
):

    if not settings.WEATHER_API_KEY:

        return {
            "error":
            "WEATHER_API_KEY missing"
        }

    # আপনার weather provider-এর
    # API call এখানে থাকবে।

    return {
        "city": city
    }
