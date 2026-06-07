import streamlit as st
import pandas as pd
from database import init_db
from resources import query_operations, get_summary_stats

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Operations Query Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }
    .main-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.8rem;
        font-weight: 600;
        color: #0f172a;
        letter-spacing: -0.5px;
        border-left: 4px solid #2563eb;
        padding-left: 12px;
        margin-bottom: 4px;
    }
    .subtitle {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 24px;
        padding-left: 16px;
    }
    .metric-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 8px;
    }
    .metric-label {
        font-size: 0.72rem;
        font-family: 'IBM Plex Mono', monospace;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0f172a;
        font-family: 'IBM Plex Mono', monospace;
    }
    .stDataFrame {
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px;
    }
    div[data-testid="stForm"] {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
    }
    .section-header {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.75rem;
        font-weight: 600;
        color: #2563eb;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 8px;
        margin-top: 16px;
    }
    .result-count {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        color: #475569;
        padding: 6px 0;
    }
</style>
""", unsafe_allow_html=True)

# ── Init DB ───────────────────────────────────────────────────────────────────
@st.cache_resource
def init():
    return init_db()

init()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🏦 OPERATION Query Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Search and explore government operation records</div>', unsafe_allow_html=True)

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Search Filters")

    with st.form("search_form"):
        st.markdown('<div class="section-header">Organization</div>', unsafe_allow_html=True)
        organization_name = st.text_input("Organization Name", placeholder="e.g. Ministry of Finance")
        tin = st.text_input("TIN", placeholder="e.g. TIN-0042")
        treasury_account_code = st.text_input("Treasury Account Code", placeholder="e.g. TAC-1234")

        st.markdown('<div class="section-header">Classification</div>', unsafe_allow_html=True)
        functional_classification_code = st.text_input("Functional Classification Code", placeholder="e.g. FCC-200")
        category = st.selectbox(
            "Category",
            options=["", "Capital", "Recurrent", "Development", "Emergency", "Social"],
        )

        st.markdown('<div class="section-header">Supplier</div>', unsafe_allow_html=True)
        supplier_name = st.text_input("Supplier Name", placeholder="e.g. Alpha Supplies")
        supplier_tin = st.text_input("Supplier TIN", placeholder="e.g. SUP-001")
        supplier_bank_account = st.text_input("Supplier Bank Account", placeholder="e.g. ET-100-001")
        product_name = st.text_input("Product Name", placeholder="e.g. Medical Equipment")

        st.markdown('<div class="section-header">Amount Range</div>', unsafe_allow_html=True)
        col_min, col_max = st.columns(2)
        with col_min:
            amount_min = st.number_input("Min", min_value=0.0, value=0.0, step=1000.0, format="%.0f")
        with col_max:
            amount_max = st.number_input("Max", min_value=0.0, value=0.0, step=1000.0, format="%.0f")

        st.markdown('<div class="section-header">Date Range</div>', unsafe_allow_html=True)
        date_from = st.date_input("From Date", value=None)
        date_to = st.date_input("To Date", value=None)

        st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
        limit_record = st.number_input(
            "Max Records (0 = all)",
            min_value=0,
            value=50,
            step=10,
            help="Set to 0 to return all matching records",
        )

        submitted = st.form_submit_button("🔎  Run Query", width='stretch', type="primary")

# ── Query & display ───────────────────────────────────────────────────────────
filters = {
    "organization_name": organization_name,
    "tin": tin,
    "treasury_account_code": treasury_account_code,
    "functional_classification_code": functional_classification_code,
    "category": category,
    "supplier_name": supplier_name,
    "supplier_tin": supplier_tin,
    "supplier_bank_account": supplier_bank_account,
    "product_name": product_name,
    "amount_min": amount_min,
    "amount_max": amount_max,
    "date_from": date_from,
    "date_to": date_to,
    "limit_record": limit_record,
}

# Run query on load OR on submit
if "df_result" not in st.session_state or submitted:
    with st.spinner("Querying database..."):
        st.session_state["df_result"] = query_operations(filters)

df: pd.DataFrame = st.session_state["df_result"]
stats = get_summary_stats(df)

# ── Summary metrics ───────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Records</div>
        <div class="metric-value">{stats['total_records']:,}</div>
    </div>""", unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Amount</div>
        <div class="metric-value">{stats['total_amount']:,.0f}</div>
    </div>""", unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Average Amount</div>
        <div class="metric-value">{stats['avg_amount']:,.0f}</div>
    </div>""", unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Unique Orgs</div>
        <div class="metric-value">{stats['unique_orgs']}</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ── Results table ─────────────────────────────────────────────────────────────
if df.empty:
    st.info("ℹ️ No records found. Try adjusting your search filters.")
else:
    st.markdown(
        f'<div class="result-count">Showing {len(df):,} record(s)</div>',
        unsafe_allow_html=True,
    )

    # Format Amount column for readability
    display_df = df.copy()
    if "Amount" in display_df.columns:
        display_df["Amount"] = display_df["Amount"].apply(lambda x: f"{x:,.2f}")

    st.dataframe(
        display_df,
        width='stretch',
        hide_index=True,
        height=500,
    )

    # ── Export ────────────────────────────────────────────────────────────────
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Export to CSV",
        data=csv,
        file_name="operations_export.csv",
        mime="text/csv",
    )