# Importing libraries
import pandas as pd
import streamlit as st
from color import edit
st.set_page_config(page_title="FLITO: Budget", page_icon='logo.png', layout="wide")

edit()

# --- Initialize persistent session state variables ---
if "budget" not in st.session_state:
    st.session_state["budget"] = 1000
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

with st.sidebar:
    st.logo(image='logo.png', size='large', icon_image='logo.png')
    st.divider()
    if st.button("← Back to FLITO", key="back_btn"):
        st.switch_page("E:\Coding Mohamed\Flito Extened\Flito-main\FLITO.py")

st.title("💰 Budget")
st.write("Make A Good Budget of your Trip!")

st.session_state["budget"] = st.number_input("Enter your budget:", min_value=10, value=st.session_state["budget"], step=1)

with st.form("add_expense_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        expense_name = st.text_input("Expense name", placeholder="e.g., Hotel night")
    with col2:
        expense_cost = st.number_input("Cost", min_value=0.0, value=0.0, step=1.0)
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if expense_name.strip():
            st.session_state["expenses"].append({"Expense": expense_name.strip(), "Cost": float(expense_cost)})
            st.success(f"Added: {expense_name.strip()} — ${expense_cost:.2f}")
        else:
            st.warning("Please enter a name and a non-negative cost.")

if st.session_state["expenses"]:
    to_delete = st.selectbox("Delete an expense (optional)", ["—"] + [e["Expense"] for e in st.session_state["expenses"]], index=0)
    if to_delete != "—":
        st.session_state["expenses"] = [e for e in st.session_state["expenses"] if e["Expense"] != to_delete]
        st.success(f"Deleted: {to_delete}")
        st.rerun()

    df_expenses = pd.DataFrame(st.session_state["expenses"])
    styled_df = df_expenses.style.set_properties(**{
        'background-color': "#1F284A",
        'color': "#ffffff",
        'border-color': "#CDA555"
    })
    st.dataframe(styled_df, hide_index=True)
    total_spent = float(df_expenses["Cost"].sum()) if not df_expenses.empty else 0.0
    remaining = st.session_state["budget"] - total_spent
    st.write(f"**Total Spent:** ${total_spent:,.2f}")
    st.write(f"**Remaining:** ${remaining:,.2f}")

    if st.button("Clear all expenses"):
        st.session_state["expenses"].clear()
        st.info("All expenses cleared.")
        st.rerun()
else:
    st.info("No expenses added yet.")

st.write('---')
st.caption('💰 Track your travel budget with ease')
