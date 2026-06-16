import streamlit as st

st.set_page_config(page_title="Sales Manager Incentive Calculator", page_icon="💎", layout="centered")
st.title("Sales Manager Incentive Calculator")

st.sidebar.header("Enter Details")
ar = st.sidebar.number_input("Enter Monthly Sales Amount (₹)", min_value=0, value=32500000, step=100000)

TR = 32500000

def calculate(ar):
    a = ar / TR
    if a < 0.95:
        rate = 0.0
    elif a < 1:
        rate = 0.00025
    else:
        rate = 0.0005 + 0.0003 * (a - 1)
    rate = min(rate, 0.001)
    return rate, ar * rate

rate, payout = calculate(ar)

st.subheader("Results")
col1, col2 = st.columns(2)
with col1:
    st.metric("Incentive Amount", f"₹ {payout:,.2f}")
with col2:
    st.metric("Effective Rate", f"{rate*100:.4f}%")

st.success(f"Sales Manager | Monthly Revenue: ₹{ar:,}")
