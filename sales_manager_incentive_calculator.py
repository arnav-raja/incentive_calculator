import streamlit as st

st.set_page_config(page_title="Sales Manager Incentive Calculator", page_icon="💎", layout="centered")

st.title("Sales Manager Incentive Calculator")

st.sidebar.header("Select Tier")
tier = st.sidebar.selectbox("Choose Tier", ["Gold", "Silver"])

ar = st.sidebar.number_input("Enter Monthly Sales (₹)", min_value=0, value=25000000, step=100000)

def calculate(tier, ar):
    if tier == "Gold":
        a = ar / 25000000
        if a < 0.95:
            rate = 0.0
        elif a < 1:
            rate = 0.00025
        else:
            rate = 0.0006 + 0.0002 * (a - 1)
    else:
        a = ar / 10000000
        if a < 0.95:
            rate = 0.0
        elif a < 1:
            rate = 0.00025
        else:
            rate = 0.0006 + 0.0001 * (a - 1)
    return rate, ar * rate

rate, payout = calculate(tier, ar)

st.subheader("Results")
col1, col2 = st.columns(2)
with col1:
    st.metric("Incentive Amount", f"₹ {payout:,.2f}")
with col2:
    st.metric("Effective Rate", f"{rate*100:.4f}%")

st.success(f"Sales Manager | {tier} | Monthly Sales: ₹{ar:,}")
