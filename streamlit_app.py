# soubor: ave_app.py
import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Přepočet AVE z Excelu")

uploaded_file = st.file_uploader("Nahraj Excel soubor", type=["xlsx"])

def upravit_ave(row):
    delka = row.get("Délka audia/videa (sekundy)", None)
    ave = row["AVE (advertising value equivalency)"]
    if pd.notna(delka):
        if 1 <= delka <= 1800:
            return ave * 0.01
        elif 1801 <= delka <= 3600:
            return ave * 0.008
        elif 3601 <= delka <= 7200:
            return ave * 0.005
        elif 7201 <= delka <= 10800:
            return ave * 0.003
        elif delka > 10801:
            return ave * 0.001
    return ave  # nezměněné, pokud nespadá do rozsahu nebo je prázdné

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()  # očista názvů sloupců

    # Přepočet AVE
    df["AVE (advertising value equivalency)"] = df.apply(upravit_ave, axis=1)

    # Výstup
    st.success("Soubor byl zpracován.")

    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    st.download_button(
        label="Stáhnout upravený Excel",
        data=output,
        file_name="upraveny_AVE.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
