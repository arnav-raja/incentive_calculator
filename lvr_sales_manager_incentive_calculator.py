import streamlit as st

st.set_page_config(page_title="LVR Sales Manager Incentive Calculator", page_icon="💎", layout="centered")
st.title("LVR Sales Manager Incentive Calculator")
st.sidebar.header("Enter Details")

ar = st.sidebar.number_input("Enter Monthly Sales Amount (₹)", min_value=0, value=25000000, step=100000)
TR = 25000000
MIN_PAYOUT = 15000
SLOPE = 0.0005
CAP_RATE = 0.001

def calculate(ar, TR):
    a = ar / TR
    if a < 0.95:
        payout = 0.0
    elif a < 1.0:
        payout = MIN_PAYOUT * (a - 0.95) / 0.05
    else:
        payout = MIN_PAYOUT + SLOPE * TR * (a - 1)
    cap = CAP_RATE * ar
    payout = min(payout, cap)
    effective_rate = payout / ar if ar > 0 else 0
    return effective_rate, payout

rate, payout = calculate(ar, TR)

st.subheader("Results")
col1, col2 = st.columns(2)
with col1:
    st.metric("Incentive Amount", f"₹ {payout:,.2f}")
with col2:
    st.metric("Effective Rate", f"{rate*100:.4f}%")

st.success(f"LVR Sales Manager | Monthly Revenue: ₹{ar:,}")
