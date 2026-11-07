import pandas as pd
import streamlit as st

def apply_dynamic_filters(records):
    if not records:
        return pd.DataFrame()
    df = pd.json_normalize(records, sep=".")
    for hidden in ("created_at", "updated_at"):
        if hidden in df.columns:
            df = df.drop(columns=[hidden])
    st.sidebar.subheader("Dynamic filters")
    filtered = df.copy()
    for column in list(df.columns):
        if column == "id":
            continue
        series = df[column].dropna()
        if series.empty:
            continue
        unique = series.astype(str).unique().tolist()
        if len(unique) <= 30 and (series.dtype == "object" or len(unique) <= 15):
            choices = sorted(unique)
            selected = st.sidebar.multiselect(f"{column}", choices, default=[])
            if selected:
                filtered = filtered[filtered[column].astype(str).isin(selected)]
        elif pd.api.types.is_numeric_dtype(series):
            low, high = float(series.min()), float(series.max())
            if low < high:
                bounds = st.sidebar.slider(f"{column} range", low, high, (low, high))
                filtered = filtered[filtered[column].between(*bounds)]
    return filtered
