
import streamlit as st
from time import sleep
import pandas as pd

df = pd.read_csv('transactions.csv')
    
# ========== PAGE TITLE ==========
st.markdown("""
<h2 style='text-align:center;color:#00E5FF;'>💳 E-Commerce Fraud Detection Dataset</h2>
<p style='text-align:center;color:lightgray;font-size:18px;'> Understanding Online Transaction Behavior to Detect Financial Fraud</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ========== DATASET STORY =============

st.markdown("""
<style>
.info-box{
background-color:#111827;
padding:18px;
border-radius:15px;
border-left:6px solid #00E5FF;
font-size:17px;
text-align:justify;
line-height:1.8;
}
</style>

<div class="info-box">
The <b>Digital Fraud Detection Dataset</b> simulates real-world online
transactions collected from customers across multiple countries, merchants,
payment channels, and devices.

Rather than focusing only on transaction amounts, this dataset captures
the complete purchasing behavior of each customer, making it suitable for
building production-ready fraud detection systems.

It contains information about
<b>customer history</b>,
<b>transaction characteristics</b>,
<b>shipping behavior</b>,
<b>merchant categories</b>,
<b>payment security</b>,
and several engineered behavioral indicators.

The target variable,
<b style="color:#00E5FF;"> is_fraud </b>,
identifies whether a transaction is Normaly or fraudulent,
allowing Machine Learning models to learn complex fraud patterns
instead of relying on simple business rules.

Because fraud represents only a very small percentage of all transactions,
the dataset reflects a realistic class imbalance similar to financial
institutions and payment gateways. 
</div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")


# ========== Quick Statistics =========

col1,col2,col3,col4=st.columns(4)

col1.metric("💳 Transactions", f"{len(df):,}")

col2.metric("📊 Features", df.shape[1]-1)

col3.metric("🌍 Countries", df["country"].nunique())

col4.metric("🛒 Merchant Categories", df["merchant_category"].nunique())

st.markdown("---")


# =========== Feature Categories =========

st.subheader("🗂 Feature Categories")

with st.expander("👤 Customer Features"):
    st.write("""
                - user_id
                - account_age_days
                - total_transactions_user
                - avg_amount_user
                - user_type """)

with st.expander("💳 Transaction Features"):
    st.write("""
                - amount
                - merchant_category
                - channel
                - promo_used
                - amount_ratio """)

with st.expander("🌍 Geographic Features"):
    st.write("""
                - country
                - bin_country
                - shipping_distance_km
                - cross_border
                - far_shipping """)

with st.expander("🔐 Security Features"):
    st.write("""
                - three_ds_flag
                - avs_match
                - security_score """)

with st.expander("📅 Time Features"):
    st.write("""
                - day_of_week
                - day_of_month
                - day_period """)

with st.expander("🎯 Target Variable"):
    st.write("- is_fraud")


# ========== COLUMN DESCRIPTIONS ==========


st.markdown("<div class='subheader'>📘 Column Descriptions</div>", unsafe_allow_html=True)

# Data dictionary (column name → description)
data_dict = {

"user_id" : "Unique customer identifier.",

"account_age_days" : "Number of days since account creation.",

"total_transactions_user" : "Historical number of transactions made by the customer.",

"avg_amount_user" : "Average historical spending of the customer.",

"amount" : "Current transaction amount.",

"country" : "Customer country.",

"bin_country" : "Country inferred from card BIN.",

"channel" : "Transaction channel (Web/App).",

"merchant_category" : "Merchant business category.",

"promo_used" : "Whether a promotion code was used.",

"three_ds_flag" : "3D Secure authentication status.",

"shipping_distance_km" : "Distance between customer and shipping destination.",

"day_of_week" : "Transaction weekday.",

"day_of_month" : "Transaction day of month.",

"day_period" : "Morning / Afternoon / Evening / Night.",

"amount_ratio" : "Transaction amount relative to customer average.",

"cross_border" : "International transaction indicator.",

"far_shipping" : "Long-distance shipping indicator.",

"user_type" : "Customer segment.",

"is_fraud" : "Target variable."}

dict_df = pd.DataFrame(list(data_dict.items()), columns=["Feature","Description"])

st.dataframe(dict_df,use_container_width=True)

st.markdown("---")


# ============= Dataset Preview ==============

st.subheader("🧾 Dataset Preview")

st.dataframe(df.head(20),use_container_width=True)

st.markdown("---")


# ============ Project Goal =============

st.subheader("🎯 Project Objective")

st.markdown("""
The objective of this project is to develop an intelligent fraud detection
system capable of distinguishing fraudulent transactions from normal ones.""")

st.markdown("---")


# ========== FOOTER ==========

st.markdown( """<center style='color:gray;font-size:18px;'> 🚀 Ready to Explore the Data? </center> """, unsafe_allow_html=True)

# ========== Navigation Buttons ==========

def go_to(page):
    st.session_state["fade"] = True
    sleep(0.3)
    st.session_state["current_page"] = page

nav1, nav2, nav3 = st.columns([1, 2, 1])
with nav1:
    if st.button("⬅️ Back"):
        go_to("home_page.py")
        st.switch_page("home_page.py")

with nav3:
    if st.button("➡️ Next"):
        go_to("pages/eda.py")
        st.switch_page("pages/eda.py")
