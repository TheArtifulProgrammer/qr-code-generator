import qrcode
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO


def create_branded_qr_code(url, logo_path, output_path="branded_qr_code.png",
                           qr_color="black", bg_color="white", logo_border=True):
    """
    Create a branded QR code with enhanced customization
    """

    # Create QR code with high error correction
    qr = qrcode.QRCode(
        version=3,  # Larger version for better logo accommodation
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    # Create QR code image
    qr_img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert('RGB')

    # Load and process logo
    if logo_path.startswith('http'):
        response = requests.get(logo_path)
        logo = Image.open(BytesIO(response.content))
    else:
        logo = Image.open(logo_path)

    # Calculate logo size
    qr_width, qr_height = qr_img.size
    logo_size = min(qr_width, qr_height) // 4

    # Resize logo
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

    if logo_border:
        # Create a circular white background for the logo
        mask_size = logo_size + 20
        mask = Image.new('L', (mask_size, mask_size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, mask_size, mask_size), fill=255)

        # Create white circular background
        logo_bg = Image.new('RGBA', (mask_size, mask_size), (255, 255, 255, 255))
        logo_bg.putalpha(mask)

        # Resize logo to fit within the circle
        inner_logo_size = logo_size - 10
        logo = logo.resize((inner_logo_size, inner_logo_size), Image.Resampling.LANCZOS)

        # Paste logo in center of circular background
        logo_pos_in_bg = ((mask_size - inner_logo_size) // 2, (mask_size - inner_logo_size) // 2)
        logo_bg.paste(logo, logo_pos_in_bg, logo if logo.mode == 'RGBA' else None)

        # Position on QR code
        final_logo = logo_bg
    else:
        final_logo = logo

    # Calculate position to center the logo
    logo_pos = ((qr_width - final_logo.size[0]) // 2, (qr_height - final_logo.size[1]) // 2)

    # Paste logo onto QR code
    qr_img.paste(final_logo, logo_pos, final_logo if final_logo.mode == 'RGBA' else None)

    # Save the result
    qr_img.save(output_path, quality=95)
    print(f"Branded QR code saved as {output_path}")

    return qr_img


# Usage for Stanbic Bank
stanbic_url = "https://digital.stanbicbank.co.zw/open-an-account/bluease-kyc-lite-account"

# Create the QR code (you'll need to provide the Stanbic logo)
create_branded_qr_code(
    url=stanbic_url,
    logo_path="stanbic_logo.png",  # Your Stanbic logo file
    output_path="stanbic_qr_code.png",
    qr_color="#1e3a8a",  # Stanbic blue color
    bg_color="white",
    logo_border=True
)