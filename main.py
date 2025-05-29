from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import qrcode
from PIL import Image, ImageDraw
import os
import uuid
from typing import Optional
import shutil

app = FastAPI(title="Custom QR Code Generator")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create directories if they don't exist
os.makedirs("static/generated", exist_ok=True)
os.makedirs("uploads", exist_ok=True)


def create_branded_qr_code(url: str, logo_path: Optional[str] = None,
                           qr_color: str = "black", bg_color: str = "white",
                           add_logo: bool = False, logo_border: bool = True):
    """
    Create a branded QR code with customization options
    """

    # Generate unique filename
    filename = f"qr_{uuid.uuid4().hex[:8]}.png"
    output_path = f"static/generated/{filename}"

    # Create QR code
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_H if add_logo else qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    # Create QR code image
    qr_img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert('RGB')

    # Add logo if requested and logo exists
    if add_logo and logo_path and os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path)

            # Calculate logo size
            qr_width, qr_height = qr_img.size
            logo_size = min(qr_width, qr_height) // 4

            # Resize logo
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

            if logo_border:
                # Create circular white background
                mask_size = logo_size + 20
                mask = Image.new('L', (mask_size, mask_size), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, mask_size, mask_size), fill=255)

                logo_bg = Image.new('RGBA', (mask_size, mask_size), (255, 255, 255, 255))
                logo_bg.putalpha(mask)

                inner_logo_size = logo_size - 10
                logo = logo.resize((inner_logo_size, inner_logo_size), Image.Resampling.LANCZOS)

                logo_pos_in_bg = ((mask_size - inner_logo_size) // 2, (mask_size - inner_logo_size) // 2)
                logo_bg.paste(logo, logo_pos_in_bg, logo if logo.mode == 'RGBA' else None)

                final_logo = logo_bg
            else:
                final_logo = logo.convert('RGBA')

            # Center logo on QR code
            logo_pos = ((qr_width - final_logo.size[0]) // 2, (qr_height - final_logo.size[1]) // 2)
            qr_img.paste(final_logo, logo_pos, final_logo)

        except Exception as e:
            print(f"Error adding logo: {e}")

    # Save the result
    qr_img.save(output_path, quality=95)

    return filename


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-qr")
async def generate_qr(
        url: str = Form(...),
        qr_color: str = Form("#000000"),
        bg_color: str = Form("#ffffff"),
        add_logo: bool = Form(False),
        logo_border: bool = Form(True),
        logo: Optional[UploadFile] = File(None)
):
    logo_path = None

    # Handle logo upload
    if add_logo and logo:
        # Save uploaded logo
        logo_filename = f"logo_{uuid.uuid4().hex[:8]}_{logo.filename}"
        logo_path = f"uploads/{logo_filename}"

        with open(logo_path, "wb") as buffer:
            shutil.copyfileobj(logo.file, buffer)

    # Generate QR code
    try:
        filename = create_branded_qr_code(
            url=url,
            logo_path=logo_path,
            qr_color=qr_color,
            bg_color=bg_color,
            add_logo=add_logo,
            logo_border=logo_border
        )

        return {
            "success": True,
            "filename": filename,
            "download_url": f"/download/{filename}"
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/download/{filename}")
async def download_qr(filename: str):
    file_path = f"static/generated/{filename}"
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type="image/png",
            filename=f"custom_qr_{filename}"
        )
    return {"error": "File not found"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)