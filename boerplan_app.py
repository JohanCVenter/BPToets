import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def calculate_projections(params, herd_data, financials, costs):
    """Perform calculations based on all user parameters."""
    herd_growth = params['% Groei van die kudde (uitbreiding)']
    speen_pct = params['% Aanteel / Speen %']
    vervangings_pct = params['% Vervangings verse (% van Verskalwer Oes)']
    cpi = params['% CPI']
    interest_rate = params['% Rente Koers']
    calf_mortality = params['% Kalf Mortaliteit% ']
    cow_mortality = params['% Mortaliteit']
    boer_aanwas_pct = params['% Verdeling met Boer OP AANWAS']
    
    # Project herd growth
    herd_data['Projected Herd'] = herd_data['Current Herd'] * (1 + herd_growth)
    herd_data['Calves'] = herd_data['Projected Herd'] * speen_pct * (1 - calf_mortality)
    herd_data['Heifers Retained'] = herd_data['Calves'] * vervangings_pct
    herd_data['Cull Cows'] = herd_data['Projected Herd'] * params['% Uitskot koeie (uitgesluit mortaliteite)']
    
    # Apply farmer's share of herd growth
    herd_data['Boer Share of Calves'] = herd_data['Calves'] * boer_aanwas_pct
    herd_data['Boer Share of Heifers'] = herd_data['Heifers Retained'] * boer_aanwas_pct
    
    # Financial projections
    financials['Projected Revenue'] = financials['Inkomste'] * (1 + herd_growth) * boer_aanwas_pct
    financials['Projected Expenses'] = financials['Maandelikse uitgawes'] * (1 + cpi)
    financials['Net Cash Flow'] = financials['Projected Revenue'] - financials['Projected Expenses']
    financials['Interest Cost'] = financials['Net Cash Flow'] * interest_rate
    
    # Cost projections
    costs['Projected Cow Cost'] = costs['Koei koste aankoop'] * (1 + cpi)
    costs['Projected Bull Cost'] = costs['Bul Koste'] * (1 + cpi)
    return herd_data, financials, costs

def main():
    st.title("BoerPlan Beta")
    
    # Sidebar inputs
    st.sidebar.header("Adjust Parameters")
    param_values = {
        '% Aanteel / Speen %': st.sidebar.slider("Speen %", 0.0, 1.0, 0.8),
        '% Groei van die kudde (uitbreiding)': st.sidebar.slider("Herd Growth %", 0.0, 0.5, 0.2),
        '% Vervangings verse (% van Verskalwer Oes)': st.sidebar.slider("Heifer Replacement %", 0.0, 1.0, 0.7),
        '% CPI': st.sidebar.slider("CPI %", 0.0, 0.1, 0.047),
        '% Rente Koers': st.sidebar.slider("Interest Rate %", 0.0, 0.2, 0.05),
        '% Kalf Mortaliteit% ': st.sidebar.slider("Calf Mortality %", 0.0, 0.2, 0.05),
        '% Mortaliteit': st.sidebar.slider("Cow Mortality %", 0.0, 0.2, 0.03),
        '% Uitskot koeie (uitgesluit mortaliteite)': st.sidebar.slider("Cull Cow %", 0.0, 0.2, 0.1),
        '% Verdeling met Boer OP AANWAS': st.sidebar.slider("Boer Share of Growth %", 0.0, 1.0, 0.5)
    }
    
    # Example datasets
    herd_data = pd.DataFrame({'Current Herd': [100, 200, 300]})
    financials = pd.DataFrame({'Inkomste': [500000, 1000000, 1500000], 'Maandelikse uitgawes': [100000, 200000, 300000]})
    costs = pd.DataFrame({'Koei koste aankoop': [14850, 16038, 17321], 'Bul Koste': [50000, 54000, 58320]})
    
    # Perform calculations
    herd_data, financials, costs = calculate_projections(param_values, herd_data, financials, costs)
    
    # Display results
    st.subheader("Projected Herd Growth")
    st.write(herd_data)
    
    st.subheader("Projected Financials")
    st.write(financials)
    
    st.subheader("Projected Costs")
    st.write(costs)
    
    # Charts
    st.subheader("Herd Growth Projection")
    plt.figure(figsize=(6, 4))
    plt.plot(herd_data.index, herd_data['Projected Herd'], marker='o', linestyle='-', label='Projected Herd')
    plt.xlabel("Year")
    plt.ylabel("Herd Size")
    plt.legend()
    st.pyplot(plt)
    
    st.subheader("Cash Flow Projection")
    plt.figure(figsize=(6, 4))
    plt.plot(financials.index, financials['Net Cash Flow'], marker='o', linestyle='-', label='Net Cash Flow', color='green')
    plt.xlabel("Year")
    plt.ylabel("Cash Flow")
    plt.legend()
    st.pyplot(plt)
    
if __name__ == "__main__":
    main()
