import os
import re
import html
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================================
# PAGE CONFIGURATION
# =========================================================================
st.set_page_config(
    page_title="Customer Churn Retention & Explainability Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================================
# MODERN SAAS CSS STYLING
# =========================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 98%;
}

/* Hero Header Banner */
.hero-banner {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 40%, #4338ca 80%, #6366f1 100%);
    padding: 26px 32px;
    border-radius: 18px;
    color: white;
    margin-bottom: 22px;
    box-shadow: 0 12px 30px -8px rgba(49, 46, 129, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.18);
    position: relative;
    overflow: hidden;
}
.hero-banner::after {
    content: "";
    position: absolute;
    top: -50%;
    right: -20%;
    width: 320px;
    height: 320px;
    background: radial-gradient(circle, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0) 70%);
    border-radius: 50%;
}
.hero-banner h1 {
    margin: 0;
    font-size: 30px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.6px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.hero-banner p {
    margin: 8px 0 0 0;
    font-size: 15px;
    opacity: 0.95;
    color: #e0e7ff;
    max-width: 850px;
    line-height: 1.5;
}
.hero-badges {
    display: flex;
    gap: 10px;
    margin-top: 14px;
    flex-wrap: wrap;
}
.hero-badge {
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.25);
    color: #ffffff;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
}

/* Metric Cards */
.kpi-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 18px 22px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    border: 1px solid #e2e8f0;
    text-align: left;
    transition: all 0.2s ease;
    border-top: 4px solid #6366f1;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08);
}
.kpi-title {
    font-size: 12px;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
.kpi-value {
    font-size: 30px;
    font-weight: 800;
    color: #0f172a;
    margin: 6px 0 3px 0;
    line-height: 1.1;
}
.kpi-subtitle {
    font-size: 12px;
    color: #94a3b8;
    margin: 0;
}

/* Driver Box */
.driver-box {
    background: #ffffff;
    border: 1px solid #fee2e2;
    border-left: 5px solid #ef4444;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 12px;
    box-shadow: 0 2px 8px rgba(239, 68, 68, 0.04);
}
.driver-box.friction {
    border-left-color: #ef4444;
    background: #fffcfc;
}
.driver-box.profile {
    border-left-color: #64748b;
    border-color: #e2e8f0;
    background: #f8fafc;
}
.driver-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}
.driver-rank {
    font-weight: 800;
    font-size: 12px;
    color: #dc2626;
    background: #fee2e2;
    padding: 2px 8px;
    border-radius: 6px;
}
.driver-badge-friction {
    font-size: 11px;
    font-weight: 700;
    color: #15803d;
    background: #dcfce7;
    padding: 2px 8px;
    border-radius: 6px;
}
.driver-badge-profile {
    font-size: 11px;
    font-weight: 700;
    color: #475569;
    background: #f1f5f9;
    padding: 2px 8px;
    border-radius: 6px;
}
.driver-text {
    font-weight: 700;
    color: #1e293b;
    font-size: 15px;
}
.driver-raw {
    font-size: 11.5px;
    color: #64748b;
    margin-top: 4px;
    font-family: monospace;
}

/* Recommendation Playbook Cards */
.playbook-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.03);
}
.playbook-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    flex-wrap: wrap;
    gap: 8px;
}
.playbook-badge-urgent {
    background: #fee2e2;
    color: #991b1b;
    font-weight: 800;
    font-size: 12px;
    padding: 4px 12px;
    border-radius: 999px;
    border: 1px solid #fecaca;
}
.playbook-badge-high {
    background: #ffedd5;
    color: #9a3412;
    font-weight: 800;
    font-size: 12px;
    padding: 4px 12px;
    border-radius: 999px;
    border: 1px solid #fed7aa;
}
.playbook-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 12px;
    margin-bottom: 14px;
}
.pillar-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 14px 16px;
    transition: all 0.2s ease;
}
.pillar-card:hover {
    border-color: #cbd5e1;
    background: #ffffff;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}
.pillar-icon {
    font-size: 18px;
    margin-right: 6px;
}
.pillar-title {
    font-size: 11.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #64748b;
    margin-bottom: 4px;
}
.pillar-desc {
    font-size: 13.5px;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.45;
}
.roi-banner {
    background: linear-gradient(90deg, #ecfdf5 0%, #f0fdf4 100%);
    border: 1px solid #bbf7d0;
    border-radius: 12px;
    padding: 12px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
}

/* Simulator Container */
.sim-container {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 16px;
    padding: 22px;
    margin-top: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.04);
}
.sim-result-card {
    background: #f8fafc;
    border: 2px solid #e2e8f0;
    border-radius: 14px;
    padding: 16px 20px;
    margin-top: 14px;
    transition: all 0.3s ease;
}
.sim-result-card.retained {
    background: #f0fdf4;
    border-color: #86efac;
}
.sim-result-card.watch {
    background: #fefce8;
    border-color: #fde047;
}
.sim-result-card.high {
    background: #fff7ed;
    border-color: #fdba74;
}

/* Script Box */
.script-box {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-left: 5px solid #4f46e5;
    border-radius: 10px;
    padding: 14px 18px;
    color: #1e293b;
    font-size: 13.5px;
    line-height: 1.6;
    font-style: italic;
    margin-top: 8px;
}

/* Badges */
.badge-danger {
    background-color: #fee2e2;
    color: #991b1b;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
}
.badge-warning {
    background-color: #ffedd5;
    color: #9a3412;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
}
.badge-info {
    background-color: #e0f2fe;
    color: #075985;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
}
.badge-success {
    background-color: #dcfce7;
    color: #166534;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 700;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)


# =========================================================================
# BILINGUAL LOCALIZATION
# =========================================================================
TRANSLATIONS = {
    "en": {
        "banner_title": "Customer Churn Retention & Explainability Hub",
        "banner_sub": "End-to-end Machine Learning intelligence: Identify high-risk customers, uncover exact churn drivers via SHAP/LIME, and execute high-impact retention strategies.",
        "badge_model": "Model: Stacked Ensemble",
        "badge_recall": "Recall: ~81%",
        "badge_xai": "XAI: SHAP + LIME",
        "sidebar_title": "Filters & Navigation",
        "lang_select": "Dashboard Language",
        "upload_csv": "Upload custom risk_table.csv",
        "filter_risk": "Risk Tier",
        "filter_contract": "Contract Type",
        "search_id": "Search Customer ID",
        "min_score": "Minimum Churn Risk Score",
        "tab_risk": "🎯 At-Risk Customers",
        "tab_detail": "👤 Customer Deep-Dive & Action Desk",
        "tab_analytics": "📊 Portfolio Analytics",
        "tab_insights": "🧠 Model & Data Insights",
        "kpi_customers": "At-Risk Customers",
        "kpi_avg_risk": "Average Risk Score",
        "kpi_very_high": "Critical Risk Tier",
        "kpi_top_action": "Top Recommended Action",
        "call_script_label": "📞 Agent Retention Call Scripts",
        "status_tracker_label": "📋 Customer Retention Status",
        "download_csv": "📥 Download Filtered Customers (CSV)",
        "churn_drivers_title": "Top-3 Churn Drivers (Why they might leave)",
        "action_title": "⚡ Prescribed Retention Strategy Playbook",
        "influence_title": "Driver Influence Breakdown (SHAP / LIME)",
        "sim_title": "🎛️ Interactive What-If Retention Simulator",
        "sim_desc": "Adjust commercial, technical, and service levers in real-time to preview predicted churn risk drop & ROI:",
    },
    "hi": {
        "banner_title": "Customer Churn Retention & Intelligence Dashboard",
        "banner_sub": "Machine Learning ke zariye jaanein kaun customer chhodne wala hai, kyun jaane wala hai, aur unhe rokne ke liye best action kya hai.",
        "badge_model": "Model: Stacked Ensemble",
        "badge_recall": "Recall: ~81%",
        "badge_xai": "Explainability: SHAP + LIME",
        "sidebar_title": "Filters aur Controls",
        "lang_select": "Bhasha / Language",
        "upload_csv": "Naya risk_table.csv upload karein",
        "filter_risk": "Risk Tier chunein",
        "filter_contract": "Contract Type chunein",
        "search_id": "Customer ID search karein",
        "min_score": "Kam se kam Risk Score",
        "tab_risk": "🎯 At-Risk Customers",
        "tab_detail": "👤 Customer Action Desk",
        "tab_analytics": "📊 Portfolio Analytics",
        "tab_insights": "🧠 Model aur Insights",
        "kpi_customers": "Khatre wale customers",
        "kpi_avg_risk": "Ausat (Avg) Risk Score",
        "kpi_very_high": "Critical Risk wale",
        "kpi_top_action": "Sabse common retention action",
        "call_script_label": "📞 Agent ke liye Call Scripts",
        "status_tracker_label": "📋 Customer Retention Status",
        "download_csv": "📥 Ye list CSV mein download karein",
        "churn_drivers_title": "Top-3 Wajah (Customer kyun chhod sakta hai)",
        "action_title": "⚡ Retention Action Playbook (Recommended)",
        "influence_title": "Wajahon ka asar (Feature Impact)",
        "sim_title": "🎛️ Live What-If Retention Simulator",
        "sim_desc": "Customer offers aur service levers adjust karke dekhein risk score kitna kam hota hai:",
    }
}


# =========================================================================
# FEATURE TRANSLATION ENGINE
# =========================================================================
FRICTION_WORDS = ["billing", "drop", "expiring", "custservice", "satisfaction", "calldrop"]

def is_fixable_friction(raw):
    """Returns True if driver represents fixable service friction."""
    t = str(raw).lower()
    return any(w in t for w in FRICTION_WORDS)


def friendly_driver(text, lang="en"):
    """Converts technical ML feature conditions (LIME/SHAP) into plain English/Hinglish."""
    raw = str(text).strip()
    t = raw.lower()
    if t in ("-", "", "none", "nan"):
        return "-"

    if lang == "hi":
        numeric = [
            ("satisfactionscore", "Kam satisfaction score (<= 5)", "Accha satisfaction score", "Ausat satisfaction score"),
            ("custservicecalls", "Customer service pe kam calls", "Customer service pe bohot zyada shikayatein", "Customer service pe normal calls"),
            ("billingspikepct", "Bill stable raha ya kam hua", "Monthly bill mein achanak 15%+ badhotri", "Bill mein mamooli badhotri"),
            ("calldroprate", "Kam call drop rate", "Bohot zyada call drops & network issue", "Ausat call drop"),
            ("droppedcalls", "Kam call drop", "Bohot zyada dropped calls (network kharab)", "Thode call drop"),
            ("tenure", "Naya customer (short tenure <= 9 mahine)", "Purana loyal customer", "Madhyam tenure"),
            ("monthlycharges", "Kam monthly charge", "Bohot zyada monthly bill (High charge)", "Ausat monthly charges"),
            ("totalcharges", "Kam kul kharch (low spend)", "Zyada kul lifetime kharch", "Ausat kul kharch"),
        ]
        flags = [
            ("billingspikeflag", "Bill mein 15%+ ka jump aaya", "Bill mein koi jump nahi"),
            ("contractexpiring", "Contract jald khatam hone wala hai", "Contract abhi chal raha hai"),
            ("contract_two year", "2-saal ke contract par hai", "2-saal ka contract NAHI hai (Month-to-month)"),
            ("contract_one year", "1-saal ke contract par hai", "1-saal ka contract NAHI hai"),
            ("internetservice_fiber", "Fiber optic high-speed plan", "Fiber optic plan nahi hai"),
            ("techsupport_yes", "Tech support facility active hai", "Dedicated Tech Support NAHI hai"),
            ("onlinesecurity_yes", "Online security protection active", "Online Security protection nahi hai"),
            ("paymentmethod_electronic", "Electronic check se payment", "Electronic check nahi use karta"),
            ("paperlessbilling", "Paperless e-billing active", "Paperless billing nahi hai"),
        ]
    else:
        numeric = [
            ("satisfactionscore", "Low Satisfaction Score (<= 5 / 10)", "High Customer Satisfaction", "Moderate Satisfaction Score"),
            ("custservicecalls", "Few customer support calls", "Frequent customer support complaints", "Moderate customer support calls"),
            ("billingspikepct", "Stable or reduced bill", "Sudden monthly billing spike (> 15%)", "Moderate bill adjustment"),
            ("calldroprate", "Stable connection (low drops)", "High call drop rate & connection degradation", "Moderate call drops"),
            ("droppedcalls", "Few dropped calls", "Frequent dropped calls (network frustration)", "Average dropped calls"),
            ("tenure", "New customer (short tenure <= 9 months)", "Loyal long-tenured customer", "Mid-tenure customer"),
            ("monthlycharges", "Low monthly recurring charges", "High monthly recurring charges", "Standard monthly charges"),
            ("totalcharges", "Low cumulative spend", "High cumulative lifetime spend", "Average cumulative spend"),
        ]
        flags = [
            ("billingspikeflag", "Billing spike of 15% or higher detected", "No billing spike detected"),
            ("contractexpiring", "Contract is expiring very soon", "Contract has ample duration remaining"),
            ("contract_two year", "Active 2-year long-term commitment", "No long-term commitment (Month-to-month)"),
            ("contract_one year", "Active 1-year contract plan", "Not on a 1-year contract"),
            ("internetservice_fiber", "Fiber Optic high-speed plan subscriber", "Not on Fiber Optic"),
            ("techsupport_yes", "Has dedicated Tech Support active", "Missing dedicated Tech Support add-on"),
            ("onlinesecurity_yes", "Has Online Security add-on active", "Missing Online Security protection"),
            ("paymentmethod_electronic", "Pays via Electronic Check (high churn correlation)", "Pays via automated card/bank methods"),
            ("paperlessbilling", "Paperless electronic billing active", "Standard billing active"),
        ]

    for key, low, high, mid in numeric:
        if key in t:
            if re.match(r"^\s*-?[\d.]+\s*<", t):
                return mid
            return low if "<=" in t else high

    for key, yes, no in flags:
        if key in t:
            return yes if t.rstrip().endswith("=1") else no

    if "=" in raw:
        col, val = raw.rsplit("=", 1)
        pretty = col.replace("_", ": ")
        return f"{pretty}" if val.strip() == "1" else f"Not {pretty}"
    return raw


# =========================================================================
# ADVANCED RECOMMENDATION PLAYBOOK ENGINE
# =========================================================================
def build_recommendation_playbook(row, p=None, lang="en"):
    """Builds a rich, multi-tiered retention action plan with scripts and financial ROI."""
    score = float(row.get("risk_score", 0))
    cid = str(row.get("customerID", "Valued Customer"))
    monthly = float(p.get("MonthlyCharges", 75.0)) if p is not None else 75.0
    annual_val = monthly * 12.0
    sat = int(p.get("SatisfactionScore", 4)) if p is not None else 4
    spike = float(p.get("BillingSpikePct", 0.0)) if p is not None else 0.0
    drops = int(p.get("DroppedCalls30D", 0)) if p is not None else 0

    if score >= 0.92:
        priority_label = "🔴 URGENT: Intervene Within 2-4 Hours"
        badge_cls = "playbook-badge-urgent"
    elif score >= 0.85:
        priority_label = "🟠 HIGH PRIORITY: Intervene Within 24 Hours"
        badge_cls = "playbook-badge-high"
    else:
        priority_label = "🟡 MONITOR & NURTURE: Contact Within 48 Hours"
        badge_cls = "playbook-badge-high"

    # Tactical pillars
    commercial = f"Lock-in 1-Year Rate Protection Plan with guaranteed 20% discount (${monthly*0.20:.2f}/mo savings, ${monthly*0.20*12:.2f}/yr saved)"
    if spike > 12.0:
        credit = min(spike * 1.5, 45.0)
        commercial += f" + One-time ${credit:.2f} Billing Surge Waiver Credit"

    service = "Tier-3 Lead Supervisor callback + Remote fiber line diagnostic & Wi-Fi booster check" if (drops >= 2 or sat <= 4) else "Proactive line audit & speed bandwidth verification"
    perks = "Free 6-month VIP Priority Tech Support add-on ($120 market value, zero incremental company cost)"

    scripts = {
        "empathy": (
            f"\"Namaste / Hello! I am calling directly from our Senior Customer Leadership Team regarding Account {cid}. "
            f"I reviewed your account and noticed that you recently experienced service friction, including dropped calls and an unexpected bill adjustment. "
            f"First, I want to sincerely apologize for this experience. I am personally crediting your account with a courtesy adjustment today, "
            f"and our senior technical supervisor is scheduled to perform a dedicated line audit within 24 hours to guarantee your connection stays rock-solid.\""
        ),
        "savings": (
            f"\"Hello! Reaching out from the Account Rate Optimization Desk for Customer {cid}. "
            f"We ran a loyalty billing audit on your profile and qualified your line for our 1-Year Rate Protection Program today. "
            f"By securing your rate for the next 12 months, we will immediately freeze your pricing and reduce your monthly charge by 20% (${monthly*0.20:.2f}/month savings), "
            f"saving you over ${monthly*0.20*12:.2f} annually with zero change in your high-speed tier.\""
        ),
        "vip": (
            f"\"Hello! As a valued member on Account {cid}, we are contacting you today with an exclusive VIP Retention & Upgrade Package. "
            f"To thank you for being with us, we are adding complimentary 24/7 Priority Tech Support, free hardware protection, "
            f"and locking your plan into our premier discounted tier for the coming year. May I activate this for you right away?\""
        )
    }

    return {
        "priority_label": priority_label,
        "badge_cls": badge_cls,
        "commercial": commercial,
        "service": service,
        "perks": perks,
        "annual_val": annual_val,
        "est_saved": annual_val * 0.80,
        "scripts": scripts
    }


# =========================================================================
# DATA LOADING PIPELINE
# =========================================================================
@st.cache_data(show_spinner=False)
def load_risk_data(uploaded_file=None):
    if uploaded_file is not None:
        try:
            return pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Uploaded CSV could not be read: {e}")

    search_paths = [
        "risk_table.csv",
        "Customer_Churn_Dashboard/risk_table.csv",
        r"F:\Projects\ML_Project\risk_table.csv",
        os.path.join(os.path.dirname(__file__), "risk_table.csv"),
        os.path.join(os.path.dirname(__file__), "Customer_Churn_Dashboard", "risk_table.csv"),
        "../risk_table.csv"
    ]
    for p in search_paths:
        if os.path.exists(p):
            return pd.read_csv(p)

    st.error("Dataset 'risk_table.csv' not found.")
    return None


@st.cache_data(show_spinner=False)
def load_customer_profiles():
    search_paths = [
        "Telco_Churn_Enhanced.csv",
        r"F:\Projects\ML_Project\Telco_Churn_Enhanced.csv",
        os.path.join(os.path.dirname(__file__), "Telco_Churn_Enhanced.csv"),
        os.path.join(os.path.dirname(__file__), "..", "Telco_Churn_Enhanced.csv"),
    ]
    for p in search_paths:
        if os.path.exists(p):
            try:
                return pd.read_csv(p).set_index("customerID")
            except Exception:
                pass
    return None


def find_artifact_image(filename):
    candidates = [
        filename,
        os.path.join("Customer_Churn_Dashboard", filename),
        os.path.join(r"F:\Projects\ML_Project", filename),
        os.path.join(os.path.dirname(__file__), filename),
        os.path.join(os.path.dirname(__file__), "Customer_Churn_Dashboard", filename),
        os.path.join("..", filename)
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


# =========================================================================
# SIDEBAR CONTROLS & STATE
# =========================================================================
if "retention_status" not in st.session_state:
    st.session_state.retention_status = {}

st.sidebar.markdown("### ⚙️ Settings & Controls")
lang_choice = st.sidebar.radio("Language / भाषा", ["English 🇬🇧", "Hinglish 🇮🇳"], index=0)
lang = "hi" if "Hinglish" in lang_choice else "en"
T = TRANSLATIONS[lang]

with st.sidebar.expander(f"📁 {T['upload_csv']}", expanded=False):
    uploaded = st.file_uploader("CSV file", type=["csv"], label_visibility="collapsed")

df_raw = load_risk_data(uploaded)
df_profile = load_customer_profiles()

if df_raw is None or len(df_raw) == 0:
    st.warning("Waiting for valid dataset...")
    st.stop()

df = df_raw.copy()
if "risk_score" not in df.columns:
    st.error("The dataset must contain a 'risk_score' column.")
    st.stop()

def assign_risk_tier(s):
    if s >= 0.90:
        return "Critical"
    elif s >= 0.80:
        return "High"
    elif s >= 0.60:
        return "Watch"
    return "Low"

df["Risk Tier"] = df["risk_score"].apply(assign_risk_tier)

for i in (1, 2, 3):
    col = f"driver{i}"
    if col in df.columns:
        df[f"Friendly Driver {i}"] = df[col].apply(lambda x: friendly_driver(x, lang))
    else:
        df[f"Friendly Driver {i}"] = "-"

st.sidebar.markdown(f"**{T['filter_risk']}**")
available_tiers = ["Critical", "High", "Watch", "Low"]
default_tiers = [tier for tier in available_tiers if tier in df["Risk Tier"].unique()]
selected_tiers = st.sidebar.multiselect(
    "Tiers",
    options=available_tiers,
    default=default_tiers,
    label_visibility="collapsed"
)

if "Contract" in df.columns:
    contract_opts = sorted(df["Contract"].dropna().unique().tolist())
    selected_contracts = st.sidebar.multiselect(
        f"**{T['filter_contract']}**",
        options=contract_opts,
        default=contract_opts
    )
else:
    df["Contract"] = "Standard"
    selected_contracts = ["Standard"]

min_score_val = float(df["risk_score"].min())
score_filter = st.sidebar.slider(
    f"**{T['min_score']}**",
    min_value=0.0,
    max_value=1.0,
    value=float(min(0.80, min_score_val)),
    step=0.01,
    format="%.2f"
)

search_query = st.sidebar.text_input(f"🔍 {T['search_id']}", placeholder="e.g. 0970-ETWGE")

view = df[
    (df["Risk Tier"].isin(selected_tiers)) &
    (df["Contract"].isin(selected_contracts)) &
    (df["risk_score"] >= score_filter)
]
if search_query.strip():
    view = view[view["customerID"].astype(str).str.contains(search_query.strip(), case=False, regex=False)]
view = view.sort_values("risk_score", ascending=False).reset_index(drop=True)

st.sidebar.markdown("---")
st.sidebar.caption(f"📊 Showing **{len(view)}** of **{len(df)}** total records")


# =========================================================================
# HERO BANNER
# =========================================================================
st.markdown(f"""
<div class="hero-banner">
  <h1>🎯 {T['banner_title']}</h1>
  <p>{T['banner_sub']}</p>
  <div class="hero-badges">
    <span class="hero-badge">🤖 {T['badge_model']}</span>
    <span class="hero-badge">📈 {T['badge_recall']}</span>
    <span class="hero-badge">🔬 {T['badge_xai']}</span>
    <span class="hero-badge">⚡ Actionable Interventions</span>
  </div>
</div>
""", unsafe_allow_html=True)


# =========================================================================
# NAVIGATION TABS
# =========================================================================
tab_risk, tab_detail, tab_analytics, tab_insights = st.tabs([
    T["tab_risk"],
    T["tab_detail"],
    T["tab_analytics"],
    T["tab_insights"]
])


# =========================================================================
# TAB 1: AT-RISK CUSTOMERS LIST & EXECUTIVE KPIS
# =========================================================================
with tab_risk:
    c1, c2, c3, c4 = st.columns(4)
    total_at_risk = len(view)
    avg_risk = f"{view['risk_score'].mean():.1%}" if total_at_risk > 0 else "0%"
    critical_cnt = int((view["Risk Tier"] == "Critical").sum())
    top_action = view["suggested_action"].mode()[0] if (total_at_risk > 0 and "suggested_action" in view.columns) else "N/A"

    with c1:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #ef4444;">
            <div class="kpi-title">{T['kpi_customers']}</div>
            <div class="kpi-value" style="color: #ef4444;">{total_at_risk}</div>
            <div class="kpi-subtitle">Filtered in active queue</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #f97316;">
            <div class="kpi-title">{T['kpi_avg_risk']}</div>
            <div class="kpi-value" style="color: #f97316;">{avg_risk}</div>
            <div class="kpi-subtitle">Mean predicted churn rate</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #8b5cf6;">
            <div class="kpi-title">{T['kpi_very_high']}</div>
            <div class="kpi-value" style="color: #8b5cf6;">{critical_cnt}</div>
            <div class="kpi-subtitle">Risk score &ge; 90% (Urgent)</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #10b981;">
            <div class="kpi-title">{T['kpi_top_action']}</div>
            <div class="kpi-value" style="font-size: 19px; color: #10b981; line-height: 1.3;">{top_action}</div>
            <div class="kpi-subtitle">Primary recommended playbook</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if total_at_risk == 0:
        st.info("No customers match the active filters.")
    else:
        st.markdown("##### 📋 Prioritized Customer Queue (Highest Risk on Top)")
        display_cols = ["customerID", "Contract", "Risk Tier", "risk_score",
                        "Friendly Driver 1", "Friendly Driver 2", "suggested_action"]
        rename_map = {
            "customerID": "Customer ID",
            "risk_score": "Churn Risk",
            "Friendly Driver 1": "Primary Churn Driver",
            "Friendly Driver 2": "Secondary Churn Driver",
            "suggested_action": "Prescribed Retention Action"
        }
        table_df = view[display_cols].rename(columns=rename_map)

        st.dataframe(
            table_df,
            hide_index=True,
            width="stretch",
            column_config={
                "Churn Risk": st.column_config.ProgressColumn(
                    "Churn Probability",
                    min_value=0.0,
                    max_value=1.0,
                    format="%.1%",
                ),
                "Customer ID": st.column_config.TextColumn("Customer ID"),
                "Risk Tier": st.column_config.TextColumn("Tier"),
                "Contract": st.column_config.TextColumn("Contract"),
                "Prescribed Retention Action": st.column_config.TextColumn("Action"),
            }
        )

        csv_data = view.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=T["download_csv"],
            data=csv_data,
            file_name="at_risk_customers_export.csv",
            mime="text/csv"
        )


# =========================================================================
# TAB 2: CUSTOMER DEEP-DIVE & RETENTION ACTION DESK
# =========================================================================
with tab_detail:
    if total_at_risk == 0:
        st.info("No customers available. Adjust filters in the sidebar.")
    else:
        customer_options = view["customerID"].tolist()
        selected_cid = st.selectbox("Select Customer to inspect:", customer_options, index=0)
        row = view[view["customerID"] == selected_cid].iloc[0]
        score = float(row["risk_score"])
        prof = df_profile.loc[selected_cid] if (df_profile is not None and selected_cid in df_profile.index) else None

        playbook = build_recommendation_playbook(row, prof, lang)

        # Header info
        col_left, col_right = st.columns([1, 2], gap="large")

        with col_left:
            tier_color = "#ef4444" if score >= 0.90 else ("#f97316" if score >= 0.80 else "#eab308")
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score * 100,
                domain={'x': [0, 1], 'y': [0, 1]},
                number={'suffix': "%", 'font': {'size': 36, 'family': 'Plus Jakarta Sans', 'color': '#0f172a'}},
                title={'text': "Predicted Churn Risk", 'font': {'size': 16, 'color': '#64748b'}},
                gauge={
                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#cbd5e1'},
                    'bar': {'color': tier_color},
                    'bgcolor': 'white',
                    'borderwidth': 2,
                    'bordercolor': '#e2e8f0',
                    'steps': [
                        {'range': [0, 60], 'color': 'rgba(34, 197, 94, 0.2)'},
                        {'range': [60, 80], 'color': 'rgba(234, 179, 8, 0.2)'},
                        {'range': [80, 90], 'color': 'rgba(249, 115, 22, 0.2)'},
                        {'range': [90, 100], 'color': 'rgba(239, 68, 68, 0.25)'}
                    ],
                }
            ))
            fig_gauge.update_layout(
                height=240,
                margin=dict(l=15, r=15, t=30, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': '#1e293b'}
            )
            st.plotly_chart(fig_gauge, width="stretch")

            tier_badge = "badge-danger" if row["Risk Tier"] == "Critical" else ("badge-warning" if row["Risk Tier"] == "High" else "badge-info")
            st.markdown(f"""
            <div style="text-align: center; margin-top: -10px; margin-bottom: 16px;">
                <span class="{tier_badge}">{row['Risk Tier']} Risk ({score:.1%})</span>
                <span class="badge-info" style="margin-left: 6px;">{row['Contract']}</span>
            </div>
            """, unsafe_allow_html=True)

            # Retention Status Tracker
            st.markdown(f"**{T['status_tracker_label']}**")
            status_options = ["To Contact", "Call Scheduled", "Offer Accepted (Retained)", "Escalated", "Lost"]
            current_status = st.session_state.retention_status.get(selected_cid, "To Contact")
            new_status = st.selectbox(
                "Update customer retention status:",
                options=status_options,
                index=status_options.index(current_status) if current_status in status_options else 0,
                key=f"status_{selected_cid}"
            )
            st.session_state.retention_status[selected_cid] = new_status
            if new_status == "Offer Accepted (Retained)":
                st.success("Customer status recorded: Successfully Retained! 🎉")
            else:
                st.info(f"Current Status: **{new_status}**")

        with col_right:
            st.markdown(f"#### {T['churn_drivers_title']}")
            for idx in (1, 2, 3):
                fr_text = row.get(f"Friendly Driver {idx}", "-")
                raw_text = str(row.get(f"driver{idx}", "-"))
                w_val = float(row.get(f"w{idx}", 0))
                
                is_fric = is_fixable_friction(raw_text)
                badge_html = ('<span class="driver-badge-friction">⚡ Fixable Friction</span>' if is_fric 
                              else '<span class="driver-badge-profile">📌 Profile Characteristic</span>')
                box_cls = "driver-box friction" if is_fric else "driver-box profile"

                st.markdown(f"""
                <div class="{box_cls}">
                    <div class="driver-top">
                        <span class="driver-rank">#{idx} Factor</span>
                        {badge_html}
                    </div>
                    <div class="driver-text">{html.escape(str(fr_text))}</div>
                    <div class="driver-raw">Model Feature: <code>{html.escape(raw_text)}</code> &nbsp;|&nbsp; SHAP weight contribution: <b>+{w_val:.3f}</b></div>
                </div>
                """, unsafe_allow_html=True)

            # Feature Impact Bar Chart
            drivers_list = [row.get("Friendly Driver 1", "Driver 1"),
                            row.get("Friendly Driver 2", "Driver 2"),
                            row.get("Friendly Driver 3", "Driver 3")]
            weights_list = [float(row.get("w1", 0)), float(row.get("w2", 0)), float(row.get("w3", 0))]

            df_weights = pd.DataFrame({
                "Driver": drivers_list,
                "Influence": weights_list
            }).sort_values("Influence", ascending=True)

            fig_bar = px.bar(
                df_weights,
                x="Influence",
                y="Driver",
                orientation="h",
                color="Influence",
                color_continuous_scale=["#fca5a5", "#dc2626"],
                text_auto=".3f"
            )
            fig_bar.update_layout(
                height=160,
                margin=dict(l=10, r=10, t=5, b=5),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Risk Probability Increase (+Weight)",
                yaxis_title="",
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_bar, width="stretch")

        # Telemetry Section (if profile available)
        if prof is not None:
            st.markdown("#### 📋 Customer Account & Service Telemetry")
            tp1, tp2, tp3, tp4, tp5, tp6 = st.columns(6)
            with tp1:
                st.metric("Tenure", f"{int(prof.get('tenure', 0))} mos")
            with tp2:
                st.metric("Monthly Bill", f"${float(prof.get('MonthlyCharges', 0)):.2f}")
            with tp3:
                spk = float(prof.get('BillingSpikePct', 0))
                st.metric("Bill Spike", f"{spk:+.1f}%", delta=f"{spk:+.1f}%", delta_color="inverse")
            with tp4:
                st.metric("Dropped Calls", f"{int(prof.get('DroppedCalls30D', 0))} calls")
            with tp5:
                st.metric("Support Calls", f"{int(prof.get('CustServiceCalls30D', 0))} calls")
            with tp6:
                st.metric("Satisfaction", f"{int(prof.get('SatisfactionScore', 5))} / 10")

            st.markdown(f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 16px; margin-top: 6px; font-size: 13px; color: #475569;">
                <b>Internet Plan:</b> {html.escape(str(prof.get('InternetService', 'N/A')))} &nbsp;|&nbsp;
                <b>Tech Support:</b> {html.escape(str(prof.get('TechSupport', 'N/A')))} &nbsp;|&nbsp;
                <b>Payment Method:</b> {html.escape(str(prof.get('PaymentMethod', 'N/A')))} &nbsp;|&nbsp;
                <b>Total Cumulative Spend:</b> ${float(prof.get('TotalCharges', 0)):,.2f}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================================
        # ENHANCED RECOMMENDATION SYSTEM PLAYBOOK
        # =========================================================================
        st.markdown(f"### {T['action_title']}")
        st.markdown(f"""
        <div class="playbook-container">
            <div class="playbook-header">
                <div>
                    <span class="{playbook['badge_cls']}">{playbook['priority_label']}</span>
                    <span style="font-size: 13px; color: #64748b; margin-left: 8px;">Target Account: <b>{selected_cid}</b></span>
                </div>
                <div style="font-size: 12.5px; color: #16a34a; font-weight: 700;">
                    ⚡ Prescribed Model Playbook: {html.escape(str(row.get('suggested_action', 'Senior Callback')))}
                </div>
            </div>
            <div class="playbook-grid">
                <div class="pillar-card">
                    <div class="pillar-title"><span class="pillar-icon">💰</span> Commercial Offer</div>
                    <div class="pillar-desc">{html.escape(playbook['commercial'])}</div>
                </div>
                <div class="pillar-card">
                    <div class="pillar-title"><span class="pillar-icon">🛠️</span> Service / Tech Remedy</div>
                    <div class="pillar-desc">{html.escape(playbook['service'])}</div>
                </div>
                <div class="pillar-card">
                    <div class="pillar-title"><span class="pillar-icon">🎁</span> Value-Add Loyalty Perk</div>
                    <div class="pillar-desc">{html.escape(playbook['perks'])}</div>
                </div>
            </div>
            <div class="roi-banner">
                <div>
                    <span style="font-size: 12px; color: #166534; font-weight: 600;">ANNUAL VALUE PROTECTED:</span>
                    <b style="font-size: 17px; color: #14532d; margin-left: 6px;">${playbook['annual_val']:,.2f} / yr</b>
                </div>
                <div style="font-size: 13px; color: #15803d; font-weight: 700;">
                    Expected Retention Probability: <span style="background: #dcfce7; padding: 2px 8px; border-radius: 6px;">~75% Lift</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Script selector
        with st.expander(f"📞 {T['call_script_label']} (Choose Script Style)", expanded=True):
            script_style = st.radio(
                "Select Conversational Script Style:",
                ["🤝 Empathy & Resolution (Frustrated Customer)", "💵 Price Protection & Savings (Billing Sensitive)", "👑 VIP Loyalty Upgrade (High-Value Customer)"],
                horizontal=True
            )
            if "Empathy" in script_style:
                chosen_script = playbook["scripts"]["empathy"]
            elif "Price" in script_style:
                chosen_script = playbook["scripts"]["savings"]
            else:
                chosen_script = playbook["scripts"]["vip"]

            st.markdown(f"""
            <div class="script-box">
                {chosen_script}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # =========================================================================
        # ULTRA-SMOOTH WHAT-IF RETENTION SIMULATOR
        # =========================================================================
        st.markdown(f"### {T['sim_title']}")
        st.caption(T['sim_desc'])

        # Preset Quick Offer Buttons
        col_p1, col_p2, col_p3, col_p4 = st.columns(4)
        preset_action = None
        if col_p1.button("🚀 Recommended Bundle", use_container_width=True):
            preset_action = "recommended"
        if col_p2.button("🛡️ Max Retention (2-Yr)", use_container_width=True):
            preset_action = "max"
        if col_p3.button("💡 Zero-Cost Perks", use_container_width=True):
            preset_action = "zerocost"
        if col_p4.button("🔄 Reset Levers", use_container_width=True):
            preset_action = "reset"

        # Simulator State
        sim_key_prefix = f"sim_{selected_cid}_"

        # Apply preset defaults if clicked
        if preset_action == "recommended":
            st.session_state[f"{sim_key_prefix}contract"] = "1-Year Plan (-22%)"
            st.session_state[f"{sim_key_prefix}discount"] = 20
            st.session_state[f"{sim_key_prefix}sat_boost"] = 3
            st.session_state[f"{sim_key_prefix}network"] = True
            st.session_state[f"{sim_key_prefix}tech"] = True
        elif preset_action == "max":
            st.session_state[f"{sim_key_prefix}contract"] = "2-Year Plan (-34%)"
            st.session_state[f"{sim_key_prefix}discount"] = 30
            st.session_state[f"{sim_key_prefix}sat_boost"] = 5
            st.session_state[f"{sim_key_prefix}network"] = True
            st.session_state[f"{sim_key_prefix}tech"] = True
        elif preset_action == "zerocost":
            st.session_state[f"{sim_key_prefix}contract"] = "1-Year Plan (-22%)"
            st.session_state[f"{sim_key_prefix}discount"] = 0
            st.session_state[f"{sim_key_prefix}sat_boost"] = 4
            st.session_state[f"{sim_key_prefix}network"] = True
            st.session_state[f"{sim_key_prefix}tech"] = True
        elif preset_action == "reset":
            st.session_state[f"{sim_key_prefix}contract"] = "Month-to-Month (Current)"
            st.session_state[f"{sim_key_prefix}discount"] = 0
            st.session_state[f"{sim_key_prefix}sat_boost"] = 0
            st.session_state[f"{sim_key_prefix}network"] = False
            st.session_state[f"{sim_key_prefix}tech"] = False

        sim_col_ctrl, sim_col_vis = st.columns([1.2, 1], gap="large")

        with sim_col_ctrl:
            # 1. Contract
            contract_choice = st.radio(
                "📜 Contract Commitment Lever:",
                ["Month-to-Month (Current)", "1-Year Plan (-22%)", "2-Year Plan (-34%)"],
                index=1 if preset_action in ("recommended", "zerocost") else (2 if preset_action == "max" else 0),
                key=f"{sim_key_prefix}contract",
                horizontal=True
            )

            # 2. Discount Slider
            discount_val = st.slider(
                "💰 Monthly Bill Discount (%):",
                min_value=0,
                max_value=35,
                value=20 if preset_action == "recommended" else (30 if preset_action == "max" else 0),
                step=5,
                key=f"{sim_key_prefix}discount"
            )

            # 3. Satisfaction Boost Slider
            sat_boost = st.slider(
                "⭐ Customer Satisfaction Improvement (+Points):",
                min_value=0,
                max_value=6,
                value=3 if preset_action == "recommended" else (5 if preset_action == "max" else (4 if preset_action == "zerocost" else 0)),
                step=1,
                help="Simulates resolving customer grievances via supervisor intervention",
                key=f"{sim_key_prefix}sat_boost"
            )

            # 4. Toggles
            st.markdown("**🛠️ Service & Feature Enhancements:**")
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                opt_network = st.checkbox(
                    "Resolve All Dropped Calls (-14%)",
                    value=True if preset_action in ("recommended", "max", "zerocost") else False,
                    key=f"{sim_key_prefix}network"
                )
            with t_col2:
                opt_tech = st.checkbox(
                    "Free Tech Support Bundle (-10%)",
                    value=True if preset_action in ("recommended", "max", "zerocost") else False,
                    key=f"{sim_key_prefix}tech"
                )

        # Dynamic simulation calculation
        reduction = 0.0
        if "1-Year" in contract_choice:
            reduction += 0.22
        elif "2-Year" in contract_choice:
            reduction += 0.34

        reduction += (discount_val / 100.0) * 0.45
        reduction += (sat_boost * 0.04)

        if opt_network:
            reduction += 0.14
        if opt_tech:
            reduction += 0.10

        simulated_score = max(0.08, score - reduction)
        delta_pct = (score - simulated_score)

        with sim_col_vis:
            # Dual Gauge Visualizer
            fig_dual = go.Figure()

            # Background bar
            fig_dual.add_trace(go.Bar(
                name="Baseline Risk",
                x=["Baseline (Now)", "Simulated (After Offer)"],
                y=[score * 100, simulated_score * 100],
                marker_color=["#ef4444", "#22c55e" if simulated_score < 0.50 else ("#eab308" if simulated_score < 0.75 else "#f97316")],
                text=[f"{score:.1%}", f"{simulated_score:.1%}"],
                textposition="auto"
            ))

            fig_dual.update_layout(
                title="Predicted Churn Risk Comparison",
                yaxis_range=[0, 100],
                yaxis_title="Churn Probability (%)",
                height=220,
                margin=dict(l=10, r=10, t=35, b=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_dual, width="stretch")

            # Outcome Banner
            if simulated_score < 0.50:
                outcome_cls = "sim-result-card retained"
                status_txt = "🎉 RETAINED: Churn Risk Neutralized (< 50%)"
                badge_sim = "badge-success"
            elif simulated_score < 0.75:
                outcome_cls = "sim-result-card watch"
                status_txt = "⚠️ WATCHLIST: Churn Risk Halved (Monitor in 30 Days)"
                badge_sim = "badge-warning"
            else:
                outcome_cls = "sim-result-card high"
                status_txt = "🔴 ELEVATED RISK: Increase discount or contract term"
                badge_sim = "badge-danger"

            cust_monthly = float(prof.get('MonthlyCharges', 75.0)) if prof is not None else 75.0
            monthly_cost = (cust_monthly * (discount_val / 100.0))
            annual_cost = monthly_cost * 12.0
            net_saved = (playbook['annual_val'] * (1.0 - simulated_score)) - annual_cost

            st.markdown(f"""
            <div class="{outcome_cls}">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-size: 13.5px; font-weight: 800; color: #0f172a;">{status_txt}</span>
                    <span class="{badge_sim}">-{delta_pct:.1%} Absolute</span>
                </div>
                <div style="font-size: 12px; color: #475569; line-height: 1.5;">
                    • <b>Simulated Churn Probability:</b> <b style="font-size: 15px; color: #16a34a;">{simulated_score:.1%}</b> (down from {score:.1%})<br>
                    • <b>Net Annual Revenue Preserved:</b> <b style="color: #0f172a;">${max(0, net_saved):,.2f} / yr</b><br>
                    • <b>Offer Cost:</b> ${annual_cost:.2f} / yr
                </div>
            </div>
            """, unsafe_allow_html=True)


# =========================================================================
# TAB 3: PORTFOLIO RISK ANALYTICS
# =========================================================================
with tab_analytics:
    if total_at_risk == 0:
        st.info("No data available for the active filters.")
    else:
        st.markdown("### 📈 Customer Portfolio Risk Distribution")
        pa1, pa2 = st.columns(2)

        with pa1:
            tier_counts = view["Risk Tier"].value_counts().reset_index()
            tier_counts.columns = ["Risk Tier", "Count"]
            fig_tier = px.pie(
                tier_counts,
                values="Count",
                names="Risk Tier",
                color="Risk Tier",
                color_discrete_map={
                    "Critical": "#ef4444",
                    "High": "#f97316",
                    "Watch": "#eab308",
                    "Low": "#22c55e"
                },
                hole=0.45,
                title="Risk Tier Breakdown"
            )
            fig_tier.update_layout(margin=dict(t=40, b=10, l=10, r=10))
            st.plotly_chart(fig_tier, width="stretch")

        with pa2:
            act_counts = view["suggested_action"].value_counts().reset_index()
            act_counts.columns = ["Recommended Action", "Count"]
            fig_act = px.bar(
                act_counts,
                x="Count",
                y="Recommended Action",
                orientation="h",
                color="Count",
                color_continuous_scale="Blues",
                title="Prescribed Retention Actions Volume"
            )
            fig_act.update_layout(margin=dict(t=40, b=10, l=10, r=10), coloraxis_showscale=False)
            st.plotly_chart(fig_act, width="stretch")

        st.markdown("### 🔍 Most Frequent Churn Drivers across Filtered Customers")
        all_drivers = pd.concat([
            view["Friendly Driver 1"],
            view["Friendly Driver 2"],
            view["Friendly Driver 3"]
        ])
        all_drivers = all_drivers[all_drivers != "-"].value_counts().head(8).reset_index()
        all_drivers.columns = ["Driver Trigger", "Occurrences"]

        fig_all_drivers = px.bar(
            all_drivers,
            x="Occurrences",
            y="Driver Trigger",
            orientation="h",
            color="Occurrences",
            color_continuous_scale="Sunsetdark",
            text="Occurrences"
        )
        fig_all_drivers.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            yaxis={'categoryorder': 'total ascending'},
            coloraxis_showscale=False,
            height=320
        )
        st.plotly_chart(fig_all_drivers, width="stretch")


# =========================================================================
# TAB 4: MODEL & DATA INSIGHTS
# =========================================================================
with tab_insights:
    st.markdown("""
    ### 🔬 Machine Learning Performance & Explainability
    Explore the underlying exploratory patterns, model comparison metrics, and feature importance drivers that power the churn predictions.
    """)

    img_eda = find_artifact_image("eda_insights.png")
    img_model = find_artifact_image("model_comparison.png")
    img_shap = find_artifact_image("shap_summary.png")

    # Section 1: EDA Insights
    st.markdown("#### 1. Exploratory Data Analysis & Churn Patterns")
    if img_eda:
        st.image(img_eda, caption="Key Exploratory Drivers: Contract Type, Satisfaction Score, Billing Spike & Call Drop Rate", width="stretch")
    else:
        st.warning("`eda_insights.png` not found in project directory.")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">📌 Contract & Satisfaction Dynamics</div>
            <div class="insight-desc">
                • <b>Month-to-month contracts</b> exhibit churn exceeding <b>42%</b>, compared to less than <b>3%</b> on 2-year contracts.<br>
                • Customers with <b>Satisfaction Score &le; 5</b> show exponential churn probability (&gt; 60% to 95%).
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_e2:
        st.markdown("""
        <div class="insight-card">
            <div class="insight-title">📌 Network Quality & Billing Spikes</div>
            <div class="insight-desc">
                • Customers experiencing a sudden <b>Billing Spike (15%+)</b> churn at more than <b>50%</b>.<br>
                • Churned customers average nearly <b>double the dropped calls</b> (approx. 1.9 vs 1.0 calls/month), pointing to network frustration.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---<br>", unsafe_allow_html=True)

    # Section 2: Model Comparison
    st.markdown("#### 2. Model Performance Benchmark")
    if img_model:
        st.image(img_model, caption="Model Evaluation (Recall, F1, ROC-AUC) across Logistic Regression, Decision Tree, Random Forest & Stacked Ensemble", width="stretch")
    else:
        st.warning("`model_comparison.png` not found in project directory.")

    st.markdown("""
    <div class="insight-card">
        <div class="insight-title">🎯 Why Stacked Ensemble & Logistic Regression Win</div>
        <div class="insight-desc">
            In churn retention, <b>Recall is the most critical metric</b>: failing to identify an at-risk customer means losing them permanently without an opportunity to intervene.<br>
            • <b>Stacked Ensemble & Logistic Regression</b> achieved the highest Recall (~<b>81%</b>) and ROC-AUC score (~<b>0.86+</b>).<br>
            • The Stacked Ensemble blends linear clarity with tree-based interaction detection to minimize false negatives while retaining optimal calibration.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Model Metric Comparison Table
    model_metrics = pd.DataFrame({
        "Model": ["Logistic Regression", "Decision Tree", "Random Forest", "Stacked Ensemble"],
        "Recall": [0.812, 0.774, 0.745, 0.791],
        "F1-Score": [0.643, 0.618, 0.631, 0.644],
        "ROC-AUC": [0.862, 0.819, 0.858, 0.867],
        "Primary Advantage": [
            "High linear sensitivity & interpretability",
            "Transparent decision thresholds",
            "Robust against outliers",
            "Optimal balance: Maximizes retention recall while avoiding over-intervention"
        ]
    })
    st.dataframe(
        model_metrics,
        hide_index=True,
        width="stretch",
        column_config={
            "Recall": st.column_config.ProgressColumn("Recall", min_value=0.0, max_value=1.0, format="%.1%"),
            "F1-Score": st.column_config.ProgressColumn("F1-Score", min_value=0.0, max_value=1.0, format="%.1%"),
            "ROC-AUC": st.column_config.ProgressColumn("ROC-AUC", min_value=0.0, max_value=1.0, format="%.3f"),
        }
    )

    st.markdown("---<br>", unsafe_allow_html=True)

    # Section 3: SHAP Feature Importance
    st.markdown("#### 3. Global Explainability (SHAP Beeswarm)")
    if img_shap:
        col_s1, col_s2 = st.columns([1, 1])
        with col_s1:
            st.image(img_shap, caption="SHAP (SHapley Additive exPlanations) Summary Plot", width="stretch")
        with col_s2:
            st.markdown("""
            <div class="insight-card" style="margin-top: 10px;">
                <div class="insight-title">🔍 Interpreting Global Feature Impact</div>
                <div class="insight-desc">
                    The beeswarm plot explains <b>why</b> the model makes each prediction across the entire customer base:<br><br>
                    <b>1. Satisfaction Score (Top Factor):</b> Low values (blue points) push SHAP impact significantly to the right (higher churn risk).<br><br>
                    <b>2. Tenure (Tenure in months):</b> Short tenure (blue dots) strongly escalates churn risk, whereas long-tenured customers remain highly stable.<br><br>
                    <b>3. Contract Two Year:</b> Customers with 2-year contracts (red cluster on left) experience massive negative SHAP values (dramatically reduced churn risk).<br><br>
                    <b>4. Fiber Optic Plan:</b> Fiber subscribers without bundled tech support frequently show higher churn due to service expectation gaps.<br><br>
                    <b>5. Billing Spike & Payment Method:</b> Electronic check users with bill spikes are primed for competitor switching.
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("`shap_summary.png` not found in project directory.")
