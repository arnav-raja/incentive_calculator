# Sales Associate Incentive Calculator
# Streamlit App For Finance Staff Use At Store Level

import streamlit as st
from calculator import compute_pair_incentives
from roster import SA_ROSTER

# Page Config
st.set_page_config(
    page_title="SA Incentive Calculator",
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
        <h2>Sales Associate Incentive Calculator</h2>
        <p>Pair Based Daily Incentive For Gold And Silver Tiers</p>
    </div>
""", unsafe_allow_html=True)

# Prepare Roster Options
sa_names = sorted(SA_ROSTER.keys())

# Input Section
st.subheader("Associate Details")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Sales Associate One**")
    sa1_name = st.selectbox("Name For SA1", options=sa_names, key="sa1")
    sa1_salary = SA_ROSTER[sa1_name]
    st.metric("Salary For SA1", f"{sa1_salary:,.0f}")

with col2:
    st.markdown("**Sales Associate Two**")
    sa2_options = [n for n in sa_names if n != sa1_name]
    sa2_name = st.selectbox("Name For SA2", options=sa2_options, key="sa2")
    sa2_salary = SA_ROSTER[sa2_name]
    st.metric("Salary For SA2", f"{sa2_salary:,.0f}")

st.divider()

# Revenue And Tier Inputs
st.subheader("Revenue And Tier")

tier = st.radio("Select Tier", options=["Gold", "Silver"], horizontal=True)

pair_revenue = st.number_input(
    "Pair Revenue",
    min_value=0.0,
    step=1000.0,
    format="%.2f",
    help="Total Revenue Earned By The Pair For The Day"
)

st.divider()

# Compute Button
if st.button("Compute Incentives", type="primary", use_container_width=True):

    if pair_revenue <= 0:
        st.warning("Please Enter A Valid Pair Revenue Greater Than Zero.")
    else:
        res1, res2 = compute_pair_incentives(
            sa1_name, sa1_salary,
            sa2_name, sa2_salary,
            pair_revenue, tier
        )

        st.subheader("Incentive Results")

        def result_card(res):
            # Determine Cap Status
            cap_active = res["i_raw"] >= res["cap"]
            cap_label = (
                '<span class="cap-warning">Cap Applied</span>'
                if cap_active else
                '<span class="cap-ok">Cap Not Reached</span>'
            )

            # Attainment Band Label
            band = "Below Target, No Incentive" if res["a"] < 1.0 else "At Or Above Target"

            return f"""
            <div class="result-card">
                <h4>{res['name']} - {res['tier']}</h4>
                <table>
                    <tr><td>Salary</td><td>{res['salary']:,.2f}</td></tr>
                    <tr><td>Target Revenue</td><td>{res['tr']:,.2f}</td></tr>
                    <tr><td>Attributed Revenue</td><td>{res['ar']:,.2f}</td></tr>
                    <tr><td>Attainment Ratio</td><td>{res['a']:.4f}, {band}</td></tr>
                    <tr><td>Slope</td><td>{res['y']:,.2f}</td></tr>
                    <tr><td>Raw Incentive</td><td>{res['i_raw']:,.2f}</td></tr>
                    <tr><td>Cap Threshold</td><td>{res['cap']:,.2f}, {cap_label}</td></tr>
                    <tr>
                        <td>Effective Incentive</td>
                        <td><span class="incentive-highlight">{res['i_effective']:,.2f}</span></td>
                    </tr>
                </table>
            </div>
            """

        col_r1, col_r2 = st.columns(2)

        with col_r1:
            st.markdown(result_card(res1), unsafe_allow_html=True)

        with col_r2:
            st.markdown(result_card(res2), unsafe_allow_html=True)

        # Summary Bar
        total = res1["i_effective"] + res2["i_effective"]
        st.markdown(f"""
            <div style="
                background: #1a3c6e;
                color: white;
                border-radius: 6px;
                padding: 14px 22px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 8px;
            ">
                <span style="font-size:0.95rem; opacity:0.85;">
                    Total Pair Incentive Payout
                </span>
                <span style="font-size:1.5rem; font-weight:700;">
                    {total:,.2f}
                </span>
            </div>
        """, unsafe_allow_html=True)

st.divider()

# Roster Management Note
with st.expander("Manage SA Roster"):
    st.markdown("""
        To Add Or Edit Associates And Their Salaries,
        Open roster.py And Update The SA Roster Dictionary.

        Format Each Line As Follows:
        Full Name Followed By A Colon And The Salary Value.

        Save The File And Push The Change To GitHub.
    """)

    st.dataframe(
        data={
            "Name": list(SA_ROSTER.keys()),
            "Salary": list(SA_ROSTER.values())
        },
        use_container_width=True,
        hide_index=True
    )
