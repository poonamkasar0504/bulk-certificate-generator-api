from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import os


def generate_certificate(
    recipient_name,
    event_name,
    event_date,
    certificate_id
):
    os.makedirs("certificates", exist_ok=True)

    file_path = f"certificates/certificate_{certificate_id}.pdf"

    c = canvas.Canvas(
        file_path,
        pagesize=A4
    )

    width, height = A4

    # Certificate border
    c.rect(
        20 * mm,
        20 * mm,
        width - 40 * mm,
        height - 40 * mm
    )

    # Title
    c.setFont("Helvetica-Bold", 28)

    c.drawCentredString(
        width / 2,
        height - 70 * mm,
        "CERTIFICATE"
    )

    # Subtitle
    c.setFont("Helvetica", 16)

    c.drawCentredString(
        width / 2,
        height - 90 * mm,
        "This certificate is proudly presented to"
    )

    # Recipient name
    c.setFont("Helvetica-Bold", 24)

    c.drawCentredString(
        width / 2,
        height - 115 * mm,
        recipient_name
    )

    # Event
    c.setFont("Helvetica", 15)

    c.drawCentredString(
        width / 2,
        height - 140 * mm,
        f"for successfully completing {event_name}"
    )

    # Date
    c.drawCentredString(
        width / 2,
        height - 160 * mm,
        f"Date: {event_date}"
    )

    c.save()

    return file_path