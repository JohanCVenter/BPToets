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
        "% CPI": st.sidebar.number_input("CPI Inflasie %", min_value=0.1, max_value=15.0, value=4.7),
        "% Rente Koers": st.sidebar.slider("Rente Koers %", min_value=1.0, max_value=20.0, value=8.0),
        "% Uitgawe verhooging (jaarliks - realisties)": st.sidebar.slider("Jaarlikse Uitgawe Verhoging %", min_value=1.0, max_value=15.0, value=5.0)
    }
    
    return start_date, projection_years, {**herd_parameters, **economic_parameters}

# Kry gebruiker insette
start_date, projection_years, parameters = create_parameters()

# Bereken finansiële sleutelsyfers volgens spreadsheet formules
parameters["Verwagte Kalf Oes"] = parameters["% Aanteel / Speen %"] / 100 * 400
parameters["Kalf Mortaliteit Verlies"] = parameters["% Kalf Mortaliteit%"] / 100 * parameters["Verwagte Kalf Oes"]
parameters["Netto Kalwers"] = parameters["Verwagte Kalf Oes"] - parameters["Kalf Mortaliteit Verlies"]
parameters["Verwagte Inkomste"] = parameters["Netto Kalwers"] * 200 * 40
parameters["Totale Voerkoste"] = 400 * 15000
parameters["Netto Wins"] = parameters["Verwagte Inkomste"] - parameters["Totale Voerkoste"]

# Kontantvloei berekening
parameters["Boerdery Netto"] = parameters["Verwagte Inkomste"] - parameters["Totale Voerkoste"]
parameters["Japie - Inkomste (Kumulatief)"] = parameters["Boerdery Netto"] * projection_years
parameters["Japie Koeie"] = 400 * (1 + parameters["% Groei van die kudde (uitbreiding)"] / 100) ** projection_years
parameters["Japie Cow Waarde"] = parameters["Japie Koeie"] * 15000

# Genereer tydreeks data
dates = pd.date_range(start=start_date, periods=projection_years * 4, freq='Q')
data = pd.DataFrame(index=dates)
data["Boerdery Netto"] = [parameters["Boerdery Netto"]] * len(dates)
data["Japie - Inkomste (Kumulatief)"] = data["Boerdery Netto"].cumsum()
data["Japie Koeie"] = [parameters["Japie Koeie"]] * len(dates)
data["Japie Cow Waarde"] = [parameters["Japie Cow Waarde"]] * len(dates)

# Wys resultate
st.subheader("Finansiële Berekeninge")
st.dataframe(data)

# Knoppie om data te herlaai
if st.button("Herbereken Data"):
    st.rerun()

# Keuse van grafiektipe
chart_type = st.radio("Kies grafiek tipe", ["Lyn Grafiek", "Staaf Grafiek"])
selected_metric = st.selectbox("Kies 'n parameter om te vertoon", ["Boerdery Netto", "Japie - Inkomste (Kumulatief)", "Japie Koeie", "Japie Cow Waarde"])

# Grafiekverbeterings met duidelike asetikette
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_xlabel("Jaar")
ax.set_ylabel("Bedrag (miljoene N$)")

if chart_type == "Lyn Grafiek":
    ax.plot(data.index, data[selected_metric] / 1_000_000, label=selected_metric)
else:
    ax.bar(data.index, data[selected_metric] / 1_000_000, label=selected_metric)

ax.legend()
st.pyplot(fig)

# Bykomende insigte
st.subheader("Analise en Vooruitsigte")
st.write("Hierdie grafiek toon die invloed van jou insette op jou finansiële resultate. Pas die waardes aan en sien hoe die finansiële posisie verander.")
