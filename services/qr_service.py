import qrcode
from io import BytesIO


def create_qr(text: str):

    qr = qrcode.QRCode()

    qr.add_data(text)

    qr.make(
        fit=True
    )

    image = qr.make_image()

    buffer = BytesIO()

    image.save(
        buffer,
        format="PNG"
    )

    buffer.seek(0)

    return buffer
