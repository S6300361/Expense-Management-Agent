import json
import pandas as pd
import streamlit as st
from agent.expense_agent import parse_expense
from agent.validator import validate_expense
from database.expense_crud import create_expense, get_all_expenses, update_expense, delete_expense
from dashboard.dynamic_filters import apply_dynamic_filters
from dashboard.analytics import render_analytics
from config.settings import DEFAULT_CURRENCY

def render_dashboard():
    st.title("💳 Expense Management Agent")
    st.caption("Capture expenses with AI, store them as JSON in SQLite, and manage records.")
    tab_ai, tab_manual, tab_view, tab_manage = st.tabs(["AI entry", "Manual entry", "Dashboard", "Manage records"])

    with tab_ai:
        st.subheader("Describe an expense")
        prompt = st.text_area("Expense description", placeholder="I spent 2,500 PKR on groceries yesterday using cash.")
        if st.button("Extract expense", type="primary"):
            if not prompt.strip():
                st.warning("Enter an expense description first.")
            else:
                try:
                    expense = parse_expense(prompt)
                    st.session_state["pending_expense"] = expense.model_dump(mode="json")
                    st.success("Expense extracted. Review it before saving.")
                except Exception as exc:
                    st.error(f"Could not extract expense: {exc}")
        pending = st.session_state.get("pending_expense")
        if pending:
            st.json(pending)
            if st.button("Save extracted expense"):
                create_expense(pending)
                st.session_state.pop("pending_expense", None)
                st.success("Expense saved.")
                st.rerun()

    with tab_manual:
        st.subheader("Add expense manually")
        with st.form("manual_expense"):
            amount = st.number_input("Amount", min_value=0.01, step=100.0)
            currency = st.text_input("Currency", value=DEFAULT_CURRENCY, max_chars=3)
            category = st.text_input("Category", value="Other")
            payment = st.selectbox("Payment method", ["Cash", "Debit Card", "Credit Card", "Bank Transfer", "Mobile Wallet", "Other"])
            description = st.text_input("Description")
            expense_date = st.date_input("Date")
            vendor = st.text_input("Vendor (optional)")
            submitted = st.form_submit_button("Add expense")
            if submitted:
                try:
                    payload = {"amount": amount, "currency": currency.upper(), "category": category,
                               "payment_method": payment, "description": description,
                               "date": expense_date.isoformat(), "vendor": vendor or None}
                    validated = validate_expense(payload)
                    create_expense(validated)
                    st.success("Expense added.")
                except Exception as exc:
                    st.error(f"Please check the fields: {exc}")

    records = get_all_expenses()
    with tab_view:
        st.subheader("Expense dashboard")
        filtered = apply_dynamic_filters(records)
        render_analytics(filtered)
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        if not filtered.empty:
            st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"), "expenses.csv", "text/csv")

    with tab_manage:
        st.subheader("Update or delete an expense")
        if not records:
            st.info("No records yet.")
        else:
            options = {f'#{r["id"]} · {r.get("description", "Expense")} · {r.get("amount", "")} {r.get("currency", "")}': r for r in records}
            selected_label = st.selectbox("Choose a record", list(options))
            selected = options[selected_label]
            st.write("Current JSON")
            st.json({k:v for k,v in selected.items() if k not in ("id","created_at","updated_at")})
            editable = {k:v for k,v in selected.items() if k not in ("id","created_at","updated_at")}
            edited_text = st.text_area("Edit complete JSON", json.dumps(editable, indent=2), height=260, key=f'edit_{selected["id"]}')
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Validate and update"):
                    try:
                        updated = json.loads(edited_text)
                        validate_expense(updated)
                        update_expense(selected["id"], updated)
                        st.success("Record updated.")
                        st.rerun()
                    except Exception as exc:
                        st.error(f"Update rejected: {exc}")
            with col2:
                confirm = st.checkbox("Confirm deletion", key=f'del_confirm_{selected["id"]}')
                if st.button("Delete record", disabled=not confirm):
                    delete_expense(selected["id"])
                    st.success("Record deleted.")
                    st.rerun()
