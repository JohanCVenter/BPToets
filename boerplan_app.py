import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def calculate_herd_growth(initial_herd=400, herd_growth_rate=0.2, 
                          inflation_rate=0.047, cow_cost=14850, years=10):
    herd_size = initial_herd
    cow_price = cow_cost
    data = []
    
    for year in range(2025, 2025 + years):
        herd_size *= (1 + herd_growth_rate)
        cow_price *= (1 + inflation_rate)
        total_cost = herd_size * cow_price
        
        data.append({
            "Year": year,
            "Herd Size": round(herd_size),
            "Cow Cost": round(cow_price),
            "Total Cost": round(total_cost)
        })
    
    return pd.DataFrame(data)

def plot_herd_growth(df):
    fig, ax1 = plt.subplots()
    
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Herd Size", color="tab:blue")
    ax1.plot(df["Year"], df["Herd Size"], marker="o", color="tab:blue", label="Herd Size")
    ax1.tick_params(axis='y', labelcolor="tab:blue")
    
    ax2 = ax1.twinx()
    ax2.set_ylabel("Total Cost (ZAR)", color="tab:red")
    ax2.plot(df["Year"], df["Total Cost"], marker="s", color="tab:red", label="Total Cost")
    ax2.tick_params(axis='y', labelcolor="tab:red")
    
    fig.tight_layout()
    plt.title("Herd Growth & Cost Projection")
    plt.show()

# Run calculations
df = calculate_herd_growth()
plot_herd_growth(df)

