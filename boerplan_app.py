import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Stel app titel
st.set_page_config(page_title="BoerPlan", layout="wide")
st.title("BoerPlan - Beta Weergawe")

# Sidebar vir parameter insette
st.sidebar.header("Verander Parameters")

def create_default_parameters():
    return {
        "Aantal Beeste": st.sidebar.number_input("Aantal Beeste", min_value=10, max_value=1000, value=100),
        "Voerkoste per Bees": st.sidebar.number_input("Voerkoste per Bees (R)", min_value=100, max_value=5000, value=1500),
        "Gewigstoename per Maand": st.sidebar.number_input("Gewigstoename per Bees per Maand (kg)", min_value=1, max_value=50, value=10),
        "Markprys per kg": st.sidebar.number_input("Markprys per kg (R)", min_value=10, max_value=100, value=45)
    }

# Kry gebruiker insette
parameters = create_default_parameters()

# Bereken finansiële sleutelsyfers
parameters["Totale Voerkoste"] = parameters["Aantal Beeste"] * parameters["Voerkoste per Bees"]
parameters["Totale Gewigstoename"] = parameters["Aantal Beeste"] * parameters["Gewigstoename per Maand"]
parameters["Verwagte Inkomste"] = parameters["Totale Gewigstoename"] * parameters["Markprys per kg"]
parameters["Netto Wins"] = parameters["Verwagte Inkomste"] - parameters["Totale Voerkoste"]

# Wys resultate
st.subheader("Finansiële Berekeninge")
st.dataframe(pd.DataFrame(parameters, index=["Waarde"]))

# Plot resultate
fig, ax = plt.subplots()
kategorieë = ["Totale Voerkoste", "Verwagte Inkomste", "Netto Wins"]
waardes = [parameters["Totale Voerkoste"], parameters["Verwagte Inkomste"], parameters["Netto Wins"]]
ax.bar(kategorieë, waardes, color=["red", "green", "blue"])
ax.set_ylabel("Bedrag (R)")
ax.set_title("Finansiële Oorsig")
st.pyplot(fig)

# Bykomende insigte
st.subheader("Analise en Vooruitsigte")
st.write("Hierdie grafiek toon die invloed van jou insette op jou finansiële resultate. Pas die waardes aan en sien hoe die finansiële posisie verander.")
