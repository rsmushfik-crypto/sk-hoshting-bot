TOOLS = [

    {
        "id": 1,
        "slug": "ai_chat",
        "name": "AI Chat Bot",
        "category": "AI"
    },

    {
        "id": 2,
        "slug": "youtube_downloader",
        "name": "YouTube Video Downloader",
        "category": "Media"
    },

    {
        "id": 3,
        "slug": "facebook_downloader",
        "name": "Facebook Video Downloader",
        "category": "Media"
    },

    {
        "id": 4,
        "slug": "instagram_downloader",
        "name": "Instagram Reels Downloader",
        "category": "Media"
    },

    {
        "id": 5,
        "slug": "tiktok_downloader",
        "name": "TikTok Downloader",
        "category": "Media"
    },

    {
        "id": 6,
        "slug": "file_store",
        "name": "File Store",
        "category": "Storage"
    },

    {
        "id": 7,
        "slug": "url_shortener",
        "name": "URL Shortener",
        "category": "Utility"
    },

    {
        "id": 8,
        "slug": "text_to_speech",
        "name": "Text to Speech",
        "category": "AI"
    },

    {
        "id": 9,
        "slug": "speech_to_text",
        "name": "Speech to Text",
        "category": "AI"
    },

    {
        "id": 10,
        "slug": "ocr",
        "name": "Image to Text OCR",
        "category": "AI"
    },

    # বাকি tool-গুলোও একই format-এ
    # 11 থেকে 80 পর্যন্ত এখানে থাকবে।
]


def get_tool(slug: str):

    for tool in TOOLS:

        if tool["slug"] == slug:
            return tool

    return None


def get_categories():

    categories = {}

    for tool in TOOLS:

        category = tool["category"]

        categories.setdefault(
            category,
            []
        ).append(tool)

    return categories
