from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import mm
import io

def generate_pdf(data, logo_path="assets/logo.png"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    # Logo
    try:
        logo = ImageReader(logo_path)
        c.drawImage(logo, 15*mm, height - 30*mm, width=30*mm, preserveAspectRatio=True)
    except:
        pass

    c.setFont("Helvetica-Bold", 16)
    c.drawString(60*mm, height - 20*mm, "Feuille de Route Implantologique")

    y = height - 40*mm
    c.setFont("Helvetica", 11)

    # ----------------------
    # HEADER
    # ----------------------
    for k, v in data["header"].items():
        c.drawString(20*mm, y, f"{k} : {v}")
        y -= 6*mm

    y -= 5*mm
    c.line(15*mm, y, width - 15*mm, y)
    y -= 10*mm

    # ----------------------
    # IMPLANTS TABLE
    # ----------------------
    for idx, imp in enumerate(data["implants"]):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20*mm, y, f"Implant {idx + 1}")
        y -= 8*mm

        c.setFont("Helvetica", 10)
        for key, val in imp.items():
            if key == "images":
                continue
            c.drawString(25*mm, y, f"{key} : {val}")
            y -= 5*mm

        # Images
        if imp["images"]:
            for img in imp["images"]:
                if img is not None:
                    try:
                        img_reader = ImageReader(img)
                        c.drawImage(img_reader, 25*mm, y - 30*mm, width=30*mm, height=30*mm)
                        y -= 35*mm
                    except:
                        pass
        
        y -= 10*mm

        if y < 50*mm:
            c.showPage()
            y = height - 30*mm

    # ----------------------
    # OBSERVATIONS
    # ----------------------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20*mm, y, "Observations :")
    y -= 8*mm

    c.setFont("Helvetica", 10)
    for line in data["observations"].split("\n"):
        c.drawString(25*mm, y, line)
        y -= 5*mm

    c.save()
    pdf = buffer.getvalue()
    buffer.close()

    return pdf
