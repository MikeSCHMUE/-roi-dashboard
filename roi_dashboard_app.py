import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="ROI Dashboard", layout="centered")
st.title("📊 ROI Dashboard – Return on Investment")

with st.form("roi_form"):
    st.subheader("🔧 Input Parameters")
    rooms = st.number_input("Number of Rooms", min_value=1, value=6)
    price = st.number_input("Price per Night (USD)", min_value=0.0, value=120.0, step=10.0)
    occupancy = st.slider("Occupancy Rate (%)", min_value=0, max_value=100, value=70) / 100
    days = st.number_input("Days per Year", min_value=1, value=365)
    monthly_opex = st.number_input("Monthly Operating Expenses (OPEX)", min_value=0.0, value=14800.0, step=100.0)
    capex = st.number_input("Total Investment (CAPEX)", min_value=0.0, value=259000.0, step=1000.0)
    submitted = st.form_submit_button("🚀 Calculate ROI")

if submitted:
    annual_revenue = rooms * price * occupancy * days
    annual_opex = monthly_opex * 12
    profit = annual_revenue - annual_opex
    roi = (profit / capex * 100) if capex else 0

    st.subheader("📈 Calculated Metrics")
    st.write(f"**Estimated Annual Revenue:** ${annual_revenue:,.2f}")
    st.write(f"**Annual OPEX:** ${annual_opex:,.2f}")
    st.write(f"**Estimated Profit:** ${profit:,.2f}")
    st.write(f"**ROI:** {roi:.2f}%")

    st.subheader("🔥 ROI Heatmap")
    price_range = np.arange(price - 40, price + 50, 20)
    occ_range = np.linspace(0.4, 1.0, 7)
    roi_matrix = []

    for p in price_range:
        row = []
        for occ in occ_range:
            rev = rooms * p * occ * days
            prof = rev - annual_opex
            roi_val = (prof / capex * 100) if capex else 0
            row.append(round(roi_val, 2))
        roi_matrix.append(row)

    roi_df = pd.DataFrame(roi_matrix,
                          index=[f"${int(p)}" for p in price_range],
                          columns=[f"{round(o*100)}%" for o in occ_range])

    # Get matching row/col index
    price_labels = [int(p) for p in price_range]
    occ_labels = [round(o * 100) for o in occ_range]
    row_idx = price_labels.index(int(price)) if int(price) in price_labels else None
    col_idx = occ_labels.index(int(occupancy * 100)) if int(occupancy * 100) in occ_labels else None

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(roi_df, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax, cbar_kws={'label': 'ROI (%)'})

    if row_idx is not None and col_idx is not None:
        ax.add_patch(plt.Rectangle((col_idx, row_idx), 1, 1, fill=False, edgecolor='red', lw=3))

    plt.xlabel("Occupancy Rate")
    plt.ylabel("Room Price (USD)")
    plt.title("ROI (%) by Room Price and Occupancy")
    st.pyplot(fig)
