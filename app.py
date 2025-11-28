import streamlit as st
import json
from pdf_generator import generate_pdf

st.set_page_config(page_title="Feuille de route implantaires", layout="wide")

# Chargement de la configuration
with open("implants_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

st.title("🦷 Générateur de Feuille de Route Implantaire")

st.subheader("Informations du patient")
col1, col2 = st.columns(2)
with col1:
    patient_name = st.text_input("Nom du patient")
with col2:
    intervention_date = st.date_input("Date de l’intervention")

st.divider()

st.subheader("Planification – Ajout des implants")
implants = []

num_implants = st.number_input("Nombre d'implants posés", min_value=1, max_value=12, value=1)

for i in range(num_implants):
    st.markdown(f"### Implant {i+1}")
    col1, col2, col3 = st.columns(3)

    with col1:
        location = st.text_input(f"Localisation (ex : 11, 24)", key=f"loc{i}")
        diameter = st.selectbox("Diamètre", config["diameters"], key=f"diam{i}")
        length = st.selectbox("Longueur", config["lengths"], key=f"len{i}")

    with col2:
        ref = st.text_input("Référence commerciale", key=f"ref{i}")
        surgery_type = st.radio("Type de chirurgie", ["Full guidée", "Pilotée"], key=f"type{i}")
        kit = st.selectbox("Trousse utilisée", config["kits"], key=f"kit{i}")

    with col3:
        drill = st.text_input("Forêt à utiliser (si pilotée)", key=f"drill{i}")
        img = st.file_uploader("Image (optionnelle)", type=["png", "jpg"], key=f"img{i}")

    implants.append({
        "location": location,
        "diameter": diameter,
        "length": length,
        "ref": ref,
        "surgery_type": surgery_type,
        "kit": kit,
        "drill": drill,
        "image": img
    })

st.divider()

st.subheader("Remarques / Observations")
remarks = st.text_area("Remarques", height=200)

if st.button("📄 Générer PDF"):
    output_path = generate_pdf(
        patient_name,
        intervention_date,
        implants,
        remarks
    )
    st.success("PDF généré avec succès !")
    with open(output_path, "rb") as pdf:
        st.download_button("Télécharger le PDF", pdf, file_name="feuille_de_route.pdf")
