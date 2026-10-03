import hashlib
import hmac
from urllib.parse import parse_qsl

from config import settings


def validate_init_data(
    init_data: str
) -> bool:

    if not init_data:
        return False

    data = dict(parse_qsl(init_data))

    received_hash = data.pop(
        "hash",
        None
    )

    if not received_hash:
        return False

    data_check_string = "\n".join(
        f"{key}={data[key]}"
        for key in sorted(data)
    )

    secret_key = hmac.new(
        b"WebAppData",
        settings.TELEGRAM_BOT_TOKEN.encode(),
        hashlib.sha256
    ).digest()

    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(
        calculated_hash,
        received_hash
    )
