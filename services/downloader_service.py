async def download_media(
    url: str,
    platform: str
):

    return {
        "success": False,
        "message": (
            f"{platform} downloader adapter "
            "configure করতে হবে।"
        ),
        "url": url
    }
