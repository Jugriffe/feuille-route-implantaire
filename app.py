import streamlit as st
import json

# Chargement configuration
with open("implants_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

st.set_page_config(page_title="Feuille de Route Implantologique", layout="wide")

st.title("Feuille de Route Implantologique")


# ---------------------------
#  HEADER
# ---------------------------
st.header("Informations générales")

header_data = {}

for field in config["header"]:
    if field["type"] == "text":
        header_data[field["label"]] = st.text_input(field["label"])
    elif field["type"] == "static_text":
        st.markdown(f"**{field['label']} :** {field['value']}")
        header_data[field["label"]] = field["value"]


# ---------------------------
#  TABLEAU IMPLANTS
# ---------------------------
st.header("Implants")

if "implants" not in st.session_state:
    st.session_state.implants = []

# Bouton pour ajouter un implant
if st.button("➕ Ajouter un implant"):
    st.session_state.implants.append({
        "localisation": "",
        "diametre": "",
        "longueur": "",
        "marque": "",
        "reference": "",
        "type_chirurgie": "",
        "trousse": "",
        "foret": "",
        "images": [None, None, None]
    })


# Affichage du tableau dynamique
for idx, implant in enumerate(st.session_state.implants):
    st.subheader(f"Implant {idx + 1}")

    cols = st.columns(4)

    implant["localisation"] = cols[0].text_input("Localisation", key=f"loc_{idx}")
    implant["diametre"] = cols[1].text_input("Diamètre", key=f"diam_{idx}")
    implant["longueur"] = cols[2].text_input("Longueur", key=f"len_{idx}")

    marque_options = [opt for opt in next(c for c in config["implants_table"]["columns"] if c["key"] == "marque")["options"]]
    implant["marque"] = cols[3].selectbox("Marque implant", marque_options, key=f"marque_{idx}")

    cols2 = st.columns(3)
    implant["reference"] = cols2[0].text_input("Référence commerciale", key=f"ref_{idx}")

    type_options = next(c for c in config["implants_table"]["columns"] if c["key"] == "type_chirurgie")["options"]
    implant["type_chirurgie"] = cols2[1].selectbox("Type de chirurgie", type_options, key=f"type_{idx}")

    trousse_options = next(c for c in config["implants_table"]["columns"] if c["key"] == "trousse")["options"]
    implant["trousse"] = cols2[2].selectbox("Trousse utilisée", trousse_options, key=f"trousse_{idx}")

    implant["foret"] = st.text_input("Forêt (si pilotée)", key=f"foret_{idx}")

    st.markdown("**Images (3 maximum)**")
    image_cols = st.columns(3)

    for i in range(3):
        implant["images"][i] = image_cols[i].file_uploader(f"Image {i+1}", type=["png", "jpg", "jpeg"], key=f"img_{idx}_{i}")

    if st.button(f"❌ Supprimer l’implant {idx + 1}", key=f"del_{idx}"):
        st.session_state.implants.pop(idx)
        st.rerun()

    st.markdown("---")


# ---------------------------
#  OBSERVATIONS
# ---------------------------
st.header("Remarques / Observations")

observations = st.text_area(config["observations"]["label"])


# ---------------------------
#  VALIDATION
# ---------------------------
if st.button("📄 Générer le PDF"):
    data = {
        "header": header_data,
        "implants": st.session_state.implants,
        "observations": observations
    }

    pdf_bytes = generate_pdf(data)

    st.download_button(
        label="⬇️ Télécharger le PDF",
        data=pdf_bytes,
        file_name="feuille_de_route.pdf",
        mime="application/pdf"
    )

    st.success("PDF généré avec succès !")