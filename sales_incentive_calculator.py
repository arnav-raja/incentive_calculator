import streamlit as st

st.set_page_config(page_title="Sales Incentive Calculator", page_icon="💎", layout="centered")

st.title("Sales Incentive Calculator")

st.sidebar.header("Enter Details")
tier = st.sidebar.selectbox("Choose Metal", ["Gold", "Silver"])

ar = st.sidebar.number_input("Enter Sales Amount (₹)", min_value=0, value=300000, step=10000)

def calculate(metal, ar):
    if metal == "Gold":
        a = ar / 300000
        if a < 0.95:
            rate = 0.0
        elif a < 1:
            rate = 0.00025          # Flat rate from 95% to 100%
        else:
            rate = 0.0005 + 0.0003 * (a - 1)
    else:
        a = ar / 50000
        if a < 0.95:
            rate = 0.0
        elif a < 1:
            rate = 0.0025           # Flat rate from 95% to 100%
        else:
            rate = 0.005 + 0.003 * (a - 1)
    return rate, ar * rate

rate, payout = calculate(metal, ar)

st.subheader("Results")
col1, col2 = st.columns(2)
with col1:
    st.metric("Incentive Amount", f"₹ {payout:,.2f}")
with col2:
    st.metric("Effective Rate", f"{rate*100:.4f}%")

st.success(f"{metal} | AR: ₹{ar:,}")
