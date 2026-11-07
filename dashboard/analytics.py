import pandas as pd
import plotly.express as px
import streamlit as st

def render_analytics(df):
    if df.empty or "amount" not in df.columns:
        st.info("Add expenses with an amount to see analytics.")
        return
    numeric = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    c1, c2 = st.columns(2)
    c1.metric("Total shown", f"{numeric.sum():,.2f}")
    c2.metric("Records shown", len(df))
    if "category" in df.columns:
        chart_data = df.assign(amount=numeric).groupby("category", as_index=False)["amount"].sum()
        st.plotly_chart(px.bar(chart_data, x="category", y="amount", title="Spending by category"), use_container_width=True)
