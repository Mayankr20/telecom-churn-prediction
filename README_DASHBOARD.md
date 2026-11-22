# 🎯 Customer Churn Retention & Explainability Dashboard

An intuitive, modern, attractive, and user-friendly Machine Learning dashboard built to detect at-risk customers, explain exact churn root causes with **SHAP & LIME**, and empower customer success teams with **actionable retention scripts** and a **real-time What-If simulator**.

---

## ⚡ Quick Start (1-Click Run)

### Method 1: Double-Click Launcher (Windows)
Double-click **`run_dashboard.bat`** to start:
- Option `[1]`: Launches the **Streamlit Web App** (`app.py`) on `http://localhost:8501`.
- Option `[2]`: Opens the **Standalone Zero-Install Web Dashboard** (`dashboard.html`) in your default browser.

### Method 2: Command Line
```bash
python -m streamlit run app.py
```
Or open `dashboard.html` directly by double-clicking it.

---

## 🌟 Key Dashboard Features

### 1. 🎯 Priority At-Risk Customer Queue (Tab 1)
- **Executive KPIs**: Real-time summary of total at-risk count, mean churn risk percentage, count of critical customers (risk &ge; 90%), and top prescribed retention action.
- **Interactive Data Table**: Prioritized table sorted by risk score with live progress bars for churn probabilities.
- **Plain-English Feature Translation**: Translates cryptic ML features (e.g. `tenure <= 9.00`, `Contract_Two year=0`) into readable customer insights.
- **Search & Multi-Filter**: Instantly filter by Customer ID, Risk Tier, Contract type, or minimum risk score.
- **1-Click CSV Export**: Download the prioritized customer intervention list as `at_risk_customers_export.csv`.

### 2. 👤 Customer Deep-Dive & Action Desk (Tab 2)
- **Visual Churn Gauge Meter**: Color-coded gauge showing predicted churn probability (0% to 100%).
- **Top-3 Churn Drivers**: Clear cards highlighting the primary reasons why this specific customer is leaving, complete with:
  - Distinction between *Fixable Service Friction* (billing spikes, dropped calls) vs. *Profile Characteristics* (short tenure, contract type).
  - Model feature condition and exact **SHAP weight contribution**.
- **Prescribed Retention Action**: Clear operational recommendation (e.g., *Senior agent callback*, *Offer 1-year plan with discount*, *Bill review call*).
- **Ready-to-Use Retention Call Scripts**: Tailored conversational scripts for customer care agents (supports both **English** and **Hinglish**).
- **Driver Influence Breakdown**: Horizontal bar chart visualizing the relative impact of each driver.
- **Interactive What-If Retention Simulator**:
  - Check planned retention offers (e.g., *1-Year Contract Lock*, *Senior Tech Callback*, *20% Rate Discount*, *Free Tech Support*).
  - Dynamically recalculates and previews the customer's post-retention churn risk reduction in real-time.
- **Live Status Tracker**: Track customer progress (*To Contact*, *Call Scheduled*, *Offer Accepted (Retained)*, *Escalated*, *Lost*).

### 3. 📊 Portfolio Analytics (Tab 3)
- **Risk Tier Breakdown**: Interactive donut chart of Critical (&ge;90%), High (80-89%), and Watch (<80%) segments.
- **Retention Action Volume**: Workload distribution showing how many customers need callbacks, plan discounts, or bill audits.
- **Top Churn Drivers Across Portfolio**: Aggregated frequency of root causes across all active customers.

### 4. 🧠 Model & Data Insights (Tab 4 - Directly Linked to ML Project)
The dashboard directly links and interprets the 3 core artifacts produced by the machine learning pipeline:

#### 📌 Phase 1: Exploratory Data Analysis (`eda_insights.png`)
- **Contract Impact**: Month-to-month contracts have a churn rate exceeding **42%**, compared to only **11%** for 1-year plans and under **3%** for 2-year contracts.
- **Satisfaction Cliff**: Customers rating satisfaction &le; 5 show exponential churn probabilities (up to 95%).
- **Billing Shock**: Billing spikes (>15%) double customer churn likelihood (from ~16% to 51%).
- **Call Drop Degradation**: Churned customers suffer almost twice the dropped calls (1.92 vs 1.02 per month).

#### 📌 Phase 2: Model Performance Benchmark (`model_comparison.png`)
- Evaluates 4 candidate models: **Logistic Regression**, **Decision Tree**, **Random Forest**, and **Stacked Ensemble**.
- **Why Stacked Ensemble wins**: Achieves optimal **Recall (~79-81%)** and highest **ROC-AUC (~0.867)**. In retention, maximizing Recall prevents costly lost customer lifetime value.

#### 📌 Phase 3: Global Explainability via SHAP (`shap_summary.png`)
- **Global Beeswarm Plot**: Unpacks the model's inner decision logic across the full customer base.
- Links global features (`SatisfactionScore`, `tenure`, `Contract_Two year`, `InternetService_Fiber optic`) directly to the per-customer drivers displayed in Tab 2.

---

## 📁 Project Structure

```
Customer_Churn_Dashboard/
├── app.py                     # Streamlit Application
├── dashboard.html             # Standalone Single-Page Web Dashboard (Zero Setup)
├── risk_table.csv             # Customer churn risk scores & LIME drivers
├── eda_insights.png           # EDA artifact: Contract, Satisfaction, Billing Spike, Dropped Calls
├── model_comparison.png       # Benchmark artifact: Recall, F1, ROC-AUC across models
├── shap_summary.png           # Explainability artifact: Global SHAP beeswarm plot
├── run_dashboard.bat          # 1-Click launcher for Windows
└── README.md                  # Comprehensive project documentation
```

---

## 🌐 Bilingual Support
Seamlessly switch between **English 🇬🇧** and **Hinglish 🇮🇳** directly from the sidebar in the Streamlit application!
