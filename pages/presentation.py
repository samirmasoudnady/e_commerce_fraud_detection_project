
import streamlit as st

PROJECT = {
    "title": "E-Commerce Fraud Detection",
    "subtitle": "End-to-End Machine Learning Pipeline for Payment Fraud",
    "author": "Samir Masoud",
    "transactions": "299,695",
    "users": "~5,900",
    "countries": "10",
    "fraud_rate": "2%",
    "best_model": "CatBoost",
    "roc_auc": "97.62%",
    "precision": "84%",
    "recall": "81%",
    "f1": "82%",
}

st.set_page_config(page_title=PROJECT["title"], page_icon="🛡️",
                    layout="wide", initial_sidebar_state="collapsed")

if "page" not in st.session_state:
    st.session_state.page = 0
 
# =====================CSS=====================
st.markdown("""
<style>
#MainMenu{visibility:hidden;} footer{visibility:hidden;} header{visibility:hidden;}
html,body,[class*="css"]{background:#08111f;color:white;font-family:Segoe UI;}
.stApp{background:radial-gradient(circle at top,#13213b,#07111f 70%);}
.title{text-align:center;font-size:48px;font-weight:800;
background:linear-gradient(90deg,#22d3ee,#38bdf8,#2dd4bf);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.subtitle{text-align:center;color:#94a3b8;font-size:18px;margin-bottom:35px;}
.section{font-size:30px;font-weight:700;margin:25px 0 15px;color:white;}
.card{background:rgba(255,255,255,.05);padding:25px;border-radius:18px;
border:1px solid rgba(255,255,255,.08);transition:.3s;height:100%;}
.card:hover{transform:translateY(-6px);border-color:#22d3ee;
box-shadow:0 0 25px rgba(34,211,238,.3);}
.kpi{text-align:center;background:rgba(255,255,255,.04);padding:18px;
border-radius:16px;border:1px solid rgba(255,255,255,.08);}
.kpi h1{margin:0;color:#22d3ee;font-size:40px;}
.kpi p{margin:5px;color:#cbd5e1;}
.badge{display:inline-block;padding:8px 16px;background:#0f766e;
border-radius:30px;margin:6px;font-size:14px;}
.footer{text-align:center;margin-top:40px;color:#64748b;}
.stat-table{width:100%;border-collapse:collapse;font-size:15px;}
.stat-table th{color:#22d3ee;text-align:left;padding:8px 10px;
border-bottom:1px solid rgba(255,255,255,.15);}
.stat-table td{padding:8px 10px;border-bottom:1px solid rgba(255,255,255,.06);
color:#e2e8f0;}
.stat-table tr:last-child td{border-bottom:none;}
.pill-good{color:#2dd4bf;font-weight:700;}
.pill-bad{color:#f87171;font-weight:700;}
</style>
""", unsafe_allow_html=True)

# =====================HELPERS=====================

def header(title, subtitle):
    st.markdown(f"<div class='title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='subtitle'>{subtitle}</div>", unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="section">{title}</div>', unsafe_allow_html=True)

def card(title, html):
    st.markdown(f'<div class="card"><h3>{title}</h3><p>{html}</p></div>',
                unsafe_allow_html=True)

def raw_card(html, center=False):
    style = ' style="text-align:center"' if center else ""
    st.markdown(f'<div class="card"{style}>{html}</div>', unsafe_allow_html=True)

def kpi(value, title):
    st.markdown(f'<div class="kpi"><h1>{value}</h1><p>{title}</p></div>',
                unsafe_allow_html=True)

def kpi_row(items):
    for col, (value, title) in zip(st.columns(len(items)), items):
        with col:
            kpi(value, title)

def card_grid(items, cols=None):
    cols = cols or len(items)
    columns = st.columns(cols)
    for i, (title, text) in enumerate(items):
        with columns[i % cols]:
            card(title, text)

def pipeline(steps, arrow="⬇"):
    body = f"<br><br>{arrow}<br><br>".join(steps)
    raw_card(f'<h3 style="text-align:center">{body}</h3>')

def table_card(title, headers, rows):
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows
    )
    html = f'<table class="stat-table"><tr>{head}</tr>{body}</table>'
    card(title, html)

# ===================SLIDES=======================

TOTAL_SLIDES = 9
page = st.session_state.page
st.progress((page + 1) / TOTAL_SLIDES)
st.write("")

# ---------- 1. COVER ----------
if page == 0:
    header(f"🛡️ {PROJECT['title']}", PROJECT["subtitle"])
    kpi_row([(PROJECT["transactions"], "Transactions"),
             (PROJECT["countries"], "Countries"),
             (PROJECT["fraud_rate"], "Fraud Rate"),
             (PROJECT["roc_auc"], "ROC AUC")])
    st.write("")
    section("📌 Business Problem")
    card("The Challenge", """Online payment systems process thousands of transactions
        every day, making manual fraud detection impractical. The goal is to accurately
        flag fraudulent transactions while minimizing disruption to legitimate customers —
        a dataset where fraud makes up only about 2% of all activity.""")
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        card("🎯 Objectives", """<ul>
            <li>Analyze transaction patterns and customer behavior.</li>
            <li>Build and compare multiple classification models.</li>
            <li>Optimize detection via feature engineering & threshold tuning.</li>
            <li>Select the best-performing model for deployment.</li></ul>""")
    with c2:
        badges = "".join(f'<span class="badge">{b}</span>' for b in
            ["Python", "Pandas", "Numpy", "Plotly", "Matplotlib",
             "Scikit-learn", "Pipeline", "SMOTE", "CatBoost", "Streamlit"])
        card("🛠 Technologies", badges)

# ---------- 2. DATASET ----------
elif page == 1:
    header("📦 Dataset Overview", "299,695 real transactions across 10 countries")
    card_grid([
        ("💳 Transaction Details", "Amount, merchant category, payment channel (Web/App), and time features derived from the raw timestamp."),
        ("🌍 Geography", "10 countries — France, US, Turkey, Poland, Spain, Italy, Romania, UK, Netherlands, Germany — plus card-issuing country for cross-border checks."),
        ("🔐 Risk Signals", "3D-Secure flag, AVS match, CVV result and promo usage captured at the point of payment."),
    ], cols=3)
    st.write("")
    card_grid([
        ("👤 Customer Profile", "Account age, total transactions per user, and average historical spend per customer."),
        ("🛒 Merchant Categories", "5 sectors: electronics, fashion, gaming, travel and grocery."),
        ("⚠ Class Imbalance", "Only ~2% of transactions are fraudulent — the central modeling challenge of this project."),
    ], cols=3)
    section("Data Quality")
    raw_card("""<ul>
        <li>✔ 299,695 rows, originally 17 columns.</li>
        <li>✔ Zero duplicate records found.</li>
        <li>✔ Zero missing values across all columns.</li>
        <li>✔ Extreme values in amount / shipping distance were kept — CatBoost handles them natively and they can signal real fraud.</li>
        </ul>""")

# ---------- 3. DATA PREP & FEATURE ENGINEERING ----------
elif page == 2:
    header("🧹 Data Preparation & Feature Engineering", "Turning raw transactions into predictive signals")
    r1 = st.columns(2)
    with r1[0]:
        card("🗑 Cleaning Steps", """
            • Dropped identifier columns (transaction_id, user_id)<br>
            • Parsed transaction_time into day_of_week, day_of_month, day_period<br>
            • Mapped country codes to full names<br>
            • Verified zero duplicates & zero nulls""")
    with r1[1]:
        card("🔧 Engineered Features", """
            • <b>amount_ratio</b> = amount ÷ user's average spend<br>
            • <b>cross_border</b> = country ≠ card issuing country<br>
            • <b>far_shipping</b> = shipping distance > 500 km<br>
            • <b>security_score</b> = AVS match + 3D-Secure flag<br>
            • <b>user_type</b> = new / regular / old (by account age)""")

    st.write("")
    section("Encoding & Scaling")
    card_grid([
        ("📏 Numeric Features", "RobustScaler — chosen specifically because it is resistant to the extreme outliers deliberately kept in amount and shipping distance."),
        ("🌍 Country Features", "BinaryEncoder for country / bin_country (10 categories each) — compact encoding vs. one-hot."),
        ("🏷 Other Categoricals", "OneHotEncoder for channel, merchant_category, day_of_week, day_period, user_type."),], cols=3)

    section("Pipeline")
    pipeline(["📂 Raw Data (299,695 rows)", "🧹 Cleaning & Time Parsing",
              "⚙ Feature Engineering", "🔄 RobustScaler / Binary / One-Hot",
              "🤖 Model Training"])

# ---------- 4. EDA INSIGHTS ----------
elif page == 3:
    header("📊 Key Insights from EDA", "What actually predicts fraud in this data")
    card_grid([
        ("🌐 Web is Riskier", "Web fraud rate <b>3.56%</b> vs App <b>0.80%</b> (χ² p < 0.001) — channel is a strong, statistically significant signal."),
        ("✈️ Cross-Border Risk", "International transactions: <b>11.28%</b> fraud rate vs <b>1.43%</b> domestic — roughly <b>8× higher</b>."),
        ("📦 Shipping Distance", "far_shipping (>500km): <b>15.89%</b> fraud vs <b>0.96%</b> — the single strongest behavioral signal, ~16× higher."), ], cols=3)

    st.write("")
    card_grid([
        ("👤 New Customers", "New users: <b>17%</b> fraud rate vs <b>~1%</b> for regular/old users — early account life is high-risk."),
        ("🌍 Country Risk", "Turkey shows the highest fraud exposure (~2.8%), followed by Romania; Germany the lowest (~1.7%)."),
        ("🕐 Time of Day", "No statistically significant effect (χ² p = 0.45) — day_period alone does <b>not</b> predict fraud."),], cols=3)

    section("Business Takeaway")
    raw_card("""Fraudulent transactions also run <b>~3.5× larger</b> in average amount
        than legitimate ones across every merchant category (e.g. electronics: $619 fraud
        vs $167 normal). These EDA findings directly justify the engineered features
        (cross_border, far_shipping, amount_ratio, user_type) used in modeling.""")

# ---------- 5. MODEL COMPARISON ----------
elif page == 4:
    header("🧪 Model Comparison", "5 algorithms, tested with and without SMOTE")
    c1, c2 = st.columns(2)
    with c1:
        table_card("Without SMOTE (F1 Score)",
            ["Model", "Train", "Test"],
            [["Logistic Regression", "70.48%", "70.31%"],
             ["Random Forest", "99.98%", "83.81%"],
             ["XGBoost", "90.48%", "81.58%"],
             ["<b>CatBoost</b>", "92.46%", "83.17%"],
             ["LightGBM", "84.81%", "80.55%"]])
    with c2:
        table_card("With SMOTE (F1 Score)",
            ["Model", "Train", "Test"],
            [["Logistic Regression", "33.71%", "33.51%"],
             ["Random Forest", "99.99%", "80.68%"],
             ["XGBoost", "88.49%", "83.25%"],
             ["<b>CatBoost</b>", "87.23%", "<span class='pill-good'>83.52%</span>"],
             ["LightGBM", "84.40%", "82.92%"]])
    section("Why CatBoost")
    raw_card("""CatBoost delivered the best and most stable Test F1 score in both setups,
        handles categorical features and outliers natively, and generalized better than
        Random Forest (which showed clear signs of overfitting at ~100% train F1).
        SMOTE improved CatBoost's test performance slightly, so it was selected as the
        final algorithm for hyperparameter tuning.""")

# ---------- 6. TUNING ----------
elif page == 5:
    header("⚙️ Fine-Tuning the Best Model", "RandomizedSearchCV over CatBoost + SMOTE")
    c1, c2 = st.columns(2)
    with c1:
        card("🏆 Best Configuration", """
            <b>learning_rate</b>: 0.05<br>
            <b>iterations</b>: 1000<br>
            <b>depth</b>: 6<br><br>
            Train F1: <b>85.99%</b> &nbsp;|&nbsp; Validation F1: <b class="pill-good">83.72%</b>""")
    with c2:
        card("⚖ Class Weights (Alternative)", """
            Tried scale_pos_weight = 44 instead of SMOTE.<br><br>
            Train F1: <b>91.17%</b> &nbsp;|&nbsp; Validation F1: <b class="pill-bad">76.92%</b><br><br>
            Clear overfitting — SMOTE generalized better and was kept as the final approach.""")
    section("Final Model")
    raw_card("""📂 Dataset (299,695 rows) → 🧹 Cleaning → ⚙ Feature Engineering →
        🔄 RobustScaler / Encoders → ⚖ SMOTE → 🤖 CatBoost (lr=0.05, depth=6, 1000 iters)
        → 📈 Threshold-Tuned Prediction""", center=True)

# ---------- 7. PERFORMANCE & THRESHOLD ----------
elif page == 6:
    header("📈 Performance & Threshold Optimization", "Balancing Precision and Recall")
    kpi_row([(PROJECT["roc_auc"], "ROC AUC"), (PROJECT["precision"], "Precision"),
             (PROJECT["recall"], "Recall"), (PROJECT["f1"], "F1 Score")])
    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        table_card("Default Threshold (0.50)",
            ["Metric", "Value"],
            [["Precision", "96%"], ["Recall", "76%"],
             ["Fraud Caught", "1,009 / 1,322"], ["False Alarms", "57"]])
    with c2:
        table_card("Tuned Threshold (0.25)",
            ["Metric", "Value"],
            [["Precision", "84%"], ["Recall", "81%"],
             ["Fraud Caught", "1,074 / 1,322"], ["False Alarms", "209"]])
    section("Top Predictive Features")
    raw_card("""far_shipping · amount_ratio · promo_used · channel = web ·
        account_age_days · day_period = Night · merchant_category = gaming — the
        model relies most heavily on exactly the signals uncovered during EDA.""")
    st.success("✔ Lowering the threshold to 0.25 catches 65 more fraud cases at a manageable rise in false alarms.")

# ---------- 8. BUSINESS IMPACT & FUTURE WORK ----------
elif page == 7:
    header("💼 Business Impact & Future Work", "From model to production decision-making")
    c1, c2 = st.columns(2)
    with c1:
        card("💰 Business Value", """
            ✔ Catches 81% of fraud automatically at 84% precision<br>
            ✔ Threshold is tunable to fit real fraud-review capacity<br>
            ✔ Feature importance gives explainable red flags for analysts<br>
            ✔ Pipeline is production-ready via a saved joblib model""")
    with c2:
        card("🚀 Future Work", """
            ✔ Compare outlier handling strategies (e.g. Winsorization)<br>
            ✔ Evaluate Ordinal Encoding for user_type (naturally ordered)<br>
            ✔ Explore further class-weight configurations<br>
            ✔ Pick the final threshold based on real business review costs""")
    section("Conclusion")
    raw_card("""This project built a complete fraud-detection pipeline — from EDA and
        feature engineering to model selection and threshold optimization — landing on
        a CatBoost model with 97.62% ROC AUC that balances catching fraud against
        disrupting genuine customers.""")

# ---------- 9. THANK YOU ----------
elif page == 8:
    st.balloons()
    header("🎉 Thank You", "Questions & Discussion")
    st.write("")
    raw_card(f"""<h2>🛡 {PROJECT['title']}</h2>
        <h3>{PROJECT['subtitle']}</h3><br> 
        <h3>Created By</h3>
        <h2 style="color:#22d3ee">{PROJECT['author']}</h2>""", center=True)

# ==========================================
# NAVIGATION
# ==========================================

st.write("")
st.write("")

left, center, right = st.columns([1, 2, 1])

with left:
    if st.button("⬅ Previous", use_container_width=True) and page > 0:
        st.session_state.page -= 1
        st.rerun()

with center:
    st.markdown(f"<h4 style='text-align:center;color:#94a3b8;'>Slide {page+1} / {TOTAL_SLIDES}</h4>",
                unsafe_allow_html=True)

with right:
    if st.button("Next ➡", use_container_width=True) and page < TOTAL_SLIDES - 1:
        st.session_state.page += 1
        st.rerun()

st.markdown(f"""
<div class="footer">
🛡 {PROJECT["title"]}<br>
Created by <b>{PROJECT["author"]}</b>
</div>
""", unsafe_allow_html=True)

# =======================
# END OF FILE
# =======================
