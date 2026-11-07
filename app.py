import streamlit as st
from dashboard.dashboard import render_dashboard

st.set_page_config(page_title="Expense Management Agent", page_icon="💳", layout="wide")
render_dashboard()
