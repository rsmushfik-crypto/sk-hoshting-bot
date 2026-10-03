import secrets
import string


def generate_password(
    length: int = 16
):

    length = max(
        8,
        min(length, 128)
    )

    chars = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*_-"
    )

    return "".join(
        secrets.choice(chars)
        for _ in range(length)
    )


def clean_text(text: str):

    return text.strip()
