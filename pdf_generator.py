from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Image
import os
from datetime import datetime

def generate_pdf(patient, date, implants, remarks):
    filename = f"feuille_de_route_{patient.replace(' ', '_')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)

    width, height = A4

    # --- LOGO (facultatif) ---
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        c.drawImage(logo_path, 1*cm, height - 3*cm, width=3*cm, preserveAspectRatio=True)

    # --- TITRE ---
    c.setFont("Helvetica-Bold", 18)
    c.drawString(6*cm, height - 2*cm, "Feuille de route implantaire")

    c.setFont("Helvetica", 12)
    c.drawString(1*cm, height - 4*cm, f"Patient : {patient}")
    c.drawString(1*cm, height - 5*cm, f"Date intervention : {date}")

    y = height - 7*cm

    # --- IMPLANTS ---
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*cm, y, "Planification des implants")
    y -= 1*cm

    c.setFont("Helvetica", 11)

    for i, imp in enumerate(implants):
        if y < 5*cm:  # Nouvelle page si trop bas
            c.showPage()
            y = height - 3*cm

        c.drawString(1*cm, y, f"Implant {i+1} : {imp['location']}  |  Ø {imp['diameter']}  |  {imp['length']} mm")
        y -= 0.6*cm
        c.drawString(1*cm, y, f"Réf : {imp['ref']}  |  Chirurgie : {imp['surgery_type']}  |  Trousse : {imp['kit']}")
        y -= 0.6*cm

        if imp["surgery_type"] == "Pilotée":
            c.drawString(1*cm, y, f"Forêt utilisé : {imp['drill']}")
            y -= 0.6*cm

        # Image éventuelle
        if imp["image"] is not None:
            img_path = f"temp_img_{i}.png"
            with open(img_path, "wb") as f:
                f.write(imp["image"].getbuffer())
            c.drawImage(img_path, 10*cm, y - 3*cm, width=5*cm, height=3*cm)
            os.remove(img_path)
            y -= 3.5*cm

        y -= 0.5*cm

    # --- REMARQUES ---
    if y < 5*cm:
        c.showPage()
        y = height - 3*cm

    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*cm, y, "Remarques / Observations")
    y -= 1*cm

    text = c.beginText(1*cm, y)
    text.setFont("Helvetica", 11)
    for line in remarks.split("\n"):
        text.textLine(line)
    c.drawText(text)

    c.save()

    return filename
