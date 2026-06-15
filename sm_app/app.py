# Sales Manager Incentive Calculator
# Streamlit App For Finance Staff Use At Regional Level

import streamlit as st
from sm_calculator import compute_sm_incentive
from roster import SM_ROSTER

# Page Config
st.set_page_config(
    page_title="SM Incentive Calculator",
    layout="centered"
)

# Custom Styling
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }

        .result-card {
            background: #f8f9fb;
            border-left: 5px solid #1a3c6e;
            border-radius: 6px;
            padding: 18px 22px;
            margin-bottom: 16px;
        }

        .result-card h4 {
            color: #1a3c6e;
            margin-bottom: 8px;
            font-size: 1.05rem;
        }

        .result-card table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.92rem;
        }

        .result-card table td {
            padding: 4px 8px;
            color: #333;
        }

        .result-card table td:first-child {
            font-weight: 600;
            color: #555;
            width: 55%;
        }

        .incentive-highlight {
            font-size: 1.4rem;
            font-weight: 700;
            color: #1a3c6e;
        }

        .cap-warning {
            color: #c0392b;
            font-size: 0.85rem;
            font-weight: 600;
        }

        .cap-ok {
            color: #27ae60;
            font-size: 0.85rem;
        }

        .app-header {
            background: #1a3c6e;
            color: white;
            padding: 20px 24px;
            border-radius: 8px;
            margin-bottom: 28px;
        }

        .app-header h2 {
            margin: 0;
            font-size: 1.4rem;
            letter-spacing: 0.5px;
        }

        .app-header p {
            margin: 4px 0 0 0;
            font-size: 0.88rem;
            opacity: 0.8;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="app-header">
        <h2>Sales Manager Incentive Calculator</h2>
        <p>Monthly Incentive, Metal Agnostic</p>
    </div>
""", unsafe_allow_html=True)

# Prepare Roster Options
sm_names = sorted(SM_ROSTER.keys())

# Input Section
st.subheader("Manager Details")

sm_name = st.selectbox("Name For SM", options=sm_names, key="sm")
sm_salary = SM_ROSTER[sm_name]
st.metric("Salary For SM", f"{sm_salary:,.0f}")

st.divider()

# Revenue Input
st.subheader("Store Revenue")

store_revenue = st.number_input(
    "Store Revenue For The Month",
    min_value=0.0,
    step=10000.0,
    format="%.2f",
    help="Total Revenue Earned By The Store For The Month"
)

st.divider()

# Compute Button
if st.button("Compute Incentive", type="primary", use_container_width=True):

    if store_revenue <= 0:
        st.warning("Please Enter A Valid Store Revenue Greater Than Zero.")
    else:
        result = compute_sm_incentive(store_revenue, sm_salary)

        st.subheader("Incentive Result")

        # Determine Cap Status
        cap_active = result["i_raw"] >= result["cap"]
        cap_label = (
            '<span class="cap-warning">Cap Applied</span>'
            if cap_active else
            '<span class="cap-ok">Cap Not Reached</span>'
        )

        # Attainment Band Label
        band = "Below Target, No Incentive" if result["a"] < 1.0 else "At Or Above Target"

        st.markdown(f"""
            <div class="result-card">
                <h4>{sm_name}</h4>
                <table>
                    <tr><td>Salary</td><td>{result['salary']:,.2f}</td></tr>
                    <tr><td>Target Revenue</td><td>{result['tr']:,.2f}</td></tr>
                    <tr><td>Store Revenue</td><td>{result['ar']:,.2f}</td></tr>
                    <tr><td>Attainment Ratio</td><td>{result['a']:.4f}, {band}</td></tr>
                    <tr><td>Slope</td><td>{result['y']:,.2f}</td></tr>
                    <tr><td>Raw Incentive</td><td>{result['i_raw']:,.2f}</td></tr>
                    <tr><td>Cap Threshold</td><td>{result['cap']:,.2f}, {cap_label}</td></tr>
                    <tr>
                        <td>Effective Incentive</td>
                        <td><span class="incentive-highlight">{result['i_effective']:,.2f}</span></td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# Roster Management Note
with st.expander("Manage SM Roster"):
    st.markdown("""
        To Add Or Edit Managers And Their Salaries,
        Open roster.py And Update The SM Roster Dictionary.

        Format Each Line As Follows:
        Full Name Followed By A Colon And The Salary Value.

        Save The File And Push The Change To GitHub.
    """)

    st.dataframe(
        data={
            "Name": list(SM_ROSTER.keys()),
            "Salary": list(SM_ROSTER.values())
        },
        use_container_width=True,
        hide_index=True
    )
