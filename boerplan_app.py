import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Stel app titel
st.set_page_config(page_title="BoerPlan", layout="wide")
st.title("BoerPlan - Beta Weergawe")

# Sidebar vir parameter insette
st.sidebar.header("Verander Parameters")

# Funksie om parameters te skep
def create_parameters():
    st.sidebar.subheader("Algemene Parameters")
    start_date = st.sidebar.date_input("Begin Datum", datetime.date.today())
    projection_years = st.sidebar.number_input("Projeksie jare", min_value=1, max_value=20, value=10)
    
    st.sidebar.subheader("Kuddegroei en Produksie")
    herd_parameters = {
        "% Aanteel / Speen %": st.sidebar.slider("Aanteel / Speen %", min_value=50.0, max_value=100.0, value=85.0),
        "% Bul/Vers Kalf": st.sidebar.slider("Bul/Vers Kalf %", min_value=40.0, max_value=60.0, value=50.0),
        "% Groei van die kudde (uitbreiding)": st.sidebar.slider("Groei van die kudde %", min_value=0.0, max_value=50.0, value=10.0),
        "% Kalf Mortaliteit%": st.sidebar.slider("Kalf Mortaliteit %", min_value=1.0, max_value=15.0, value=5.0),
        "% Mortaliteit": st.sidebar.slider("Mortaliteit %", min_value=1.0, max_value=10.0, value=3.0)
    }
    
    st.sidebar.subheader("Ekonomiese Faktore")
    economic_parameters = {
        "% CPI": st.sidebar.number_input("CPI Inflasie %", min_value=0.1, max_value=15.0, value=6.0),
        "% Rente Koers": st.sidebar.slider("Rente Koers %", min_value=1.0, max_value=20.0, value=8.0),
        "% Uitgawe verhooging (jaarliks - realisties)": st.sidebar.slider("Jaarlikse Uitgawe Verhoging %", min_value=1.0, max_value=15.0, value=5.0)
    }
    
    st.sidebar.subheader("Beginkudde en Prys")
    herd_values = {
        "Begin Aantal Kalwers aangekoop": st.sidebar.number_input("Aantal Kalwers aangekoop", min_value=0, max_value=1000, value=50),
        "Begin Aantal Koeie Sanga": st.sidebar.number_input("Aantal Koeie Sanga", min_value=10, max_value=1000, value=200),
        "Begin Prys Koeie per koei met kalf": st.sidebar.number_input("Prys per Koei met Kalf (N$)", min_value=5000, max_value=50000, value=15000),
        "Begin Prys Bul": st.sidebar.number_input("Prys per Bul (N$)", min_value=10000, max_value=100000, value=40000)
    }
    
    st.sidebar.subheader("Verkoop en Markpryse")
    market_values = {
        "Prys F1 Kalf/kg": st.sidebar.number_input("Prys per kg F1 Kalf (N$)", min_value=10, max_value=100, value=45),
        "Prys F2 Kalf/kg": st.sidebar.number_input("Prys per kg F2 Kalf (N$)", min_value=10, max_value=100, value=50),
        "Prys Sanga Kalf/kg": st.sidebar.number_input("Prys per kg Sanga Kalf (N$)", min_value=10, max_value=100, value=40),
        "Gewig Kalf met verkoop": st.sidebar.number_input("Gewig van Kalf met verkoop (kg)", min_value=50, max_value=300, value=200)
    }
    
    return start_date, projection_years, {**herd_parameters, **economic_parameters, **herd_values, **market_values}

# Kry gebruiker insette
start_date, projection_years, parameters = create_parameters()

# Bereken finansiële sleutelsyfers
parameters["Verwagte Kalf Oes"] = parameters["% Aanteel / Speen %"] / 100 * parameters["Begin Aantal Koeie Sanga"]
parameters["Kalf Mortaliteit Verlies"] = parameters["% Kalf Mortaliteit%"] / 100 * parameters["Verwagte Kalf Oes"]
parameters["Netto Kalwers"] = parameters["Verwagte Kalf Oes"] - parameters["Kalf Mortaliteit Verlies"]
parameters["Verwagte Inkomste"] = parameters["Netto Kalwers"] * parameters["Gewig Kalf met verkoop"] * parameters["Prys Sanga Kalf/kg"]
parameters["Totale Voerkoste"] = parameters["Begin Aantal Koeie Sanga"] * parameters["Begin Prys Koeie per koei met kalf"]
parameters["Netto Wins"] = parameters["Verwagte Inkomste"] - parameters["Totale Voerkoste"]

# Wys resultate
st.subheader("Finansiële Berekeninge")
st.dataframe(pd.DataFrame(parameters, index=["Waarde"]))

# Skep knoppie om data te herlaai
if st.button("Herbereken Data"):
    st.experimental_rerun()

# Plot resultate
fig, ax = plt.subplots()
kategorieë = ["Totale Voerkoste", "Verwagte Inkomste", "Netto Wins"]
waardes = [parameters["Totale Voerkoste"], parameters["Verwagte Inkomste"], parameters["Netto Wins"]]
ax.bar(kategorieë, waardes, color=["red", "green", "blue"])
ax.set_ylabel("Bedrag (N$)")
ax.set_title("Finansiële Oorsig")
st.pyplot(fig)

# Bykomende insigte
st.subheader("Analise en Vooruitsigte")
st.write("Hierdie grafiek toon die invloed van jou insette op jou finansiële resultate. Pas die waardes aan en sien hoe die finansiële posisie verander.")
