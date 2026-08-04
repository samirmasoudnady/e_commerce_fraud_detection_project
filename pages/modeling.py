
import joblib
import streamlit as st
import pandas as pd
from time import sleep

# ========== PAGE TITLE ==========
st.markdown("""<h2 style='text-align:center;color:#00E5FF;'>🧠 E-Commerce Fraud Detection Model </h2>""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
# ========== SHOW CLEAN DATASET ==========

cl_df = pd.read_csv("clean_df.csv.zip").drop(columns=["is_fraud"], axis=1)
@st.cache_data
def load_fraud_data():
    df = pd.read_csv("clean_df.csv.zip")
    return df[df["is_fraud"] == "Fraud"]
fraud_df = load_fraud_data()
st.dataframe(cl_df)
st.markdown("<hr>", unsafe_allow_html=True)  
st.markdown("""<h4 style="color:white;text-align:center;">⚠️ This the only Fraud rows in our dataset </h4>""", unsafe_allow_html=True)
st.dataframe(fraud_df)
st.markdown("<hr>", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load("catboost_th.pkl")

tab1, tab2 = st.tabs(["📂 Select from dataset", "📝 Create new data"])

with tab1:
    st.markdown("""<h4 style="color:white;text-align:center;">📂 Select from dataset</h4>""", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    row_index = st.number_input("Row index", min_value=0, max_value=len(cl_df)-1, step=1)
    new_data = cl_df.iloc[[row_index]]  
    st.write("✅ Selected row preview:")
    st.dataframe(new_data)

    # detect new data 
    data = load_model()
    model = data["model"]
    threshold = data["threshold"]

    predict_button = st.button('Detect Transaction Type', key="predict_btn")
    if predict_button:
        # Predict probability
        fraud_prob = model.predict_proba(new_data)[:, 1][0]
        # Apply Threshold
        prediction = int(fraud_prob >= threshold)
        # Display probability
        st.metric(
                  "Fraud Probability",
                  f"{fraud_prob * 100:.2f}%")
        # Display result
        if prediction == 0:
            st.success("🛍️ This Operation is Normal Transaction")
        else:
            st.error("⚠️ This Operation is Fraud Transaction")

with tab2:
    st.markdown("""<h4 style="color:white;text-align:center;">📝 Create new data</h4>""", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    
    day_of_week = st.selectbox('Day of Week', cl_df.day_of_week.unique())
    country = st.selectbox('Country', cl_df.country.unique()) 
    bin_country = st.selectbox('Bin Country', cl_df.bin_country.unique())   
    merchant_category = st.selectbox('Merchant Category', cl_df.merchant_category.unique()) 
    day_period = st.selectbox('Day Period', cl_df.day_period.unique())
    user_type = st.selectbox('User Type', cl_df.user_type.unique())
    channel = st.selectbox('Channel', cl_df.channel.unique())  

    cross_border = st.radio('Cross Border', cl_df.cross_border.unique())
    security_score = st.radio('Security Score', cl_df.security_score.unique())
    far_shipping = st.radio('Far Shipping', cl_df.far_shipping.unique())
    promo_used = st.radio('Promo Used', cl_df.promo_used.unique())
    avs_match = st.radio('AVS Match', cl_df.avs_match.unique())
    cvv_result = st.radio('CVV Result', cl_df.cvv_result.unique())
    three_ds_flag = st.radio('Three DS Flag', cl_df.three_ds_flag.unique())

    day_of_month = st.slider('Day Of Month', min_value = cl_df.day_of_month.min(), max_value = cl_df.day_of_month.max(), step = 1)
    account_age_days = st.slider('Account Age Days', min_value = cl_df.account_age_days.min(), max_value = cl_df.account_age_days.max(), step = 1)
    shipping_distance_km = st.slider('Shipping Distance (km)', min_value = float(cl_df.shipping_distance_km.min()), max_value = float(cl_df.shipping_distance_km.max()), step = 0.1)
    total_transactions_user = st.slider('Total Transactions User', min_value = cl_df.total_transactions_user.min(), max_value = cl_df.total_transactions_user.max(), step = 1)
    amount = st.slider('Amount', min_value = float(cl_df.amount.min()), max_value = float(cl_df.amount.max()), step = 0.1)
    avg_amount_user = st.slider('Average Amount User', min_value = float(cl_df.avg_amount_user.min()), max_value = float(cl_df.avg_amount_user.max()), step = 0.1)
    amount_ratio = st.slider('Amount Ratio', min_value = float(cl_df.amount_ratio.min()), max_value = float(cl_df.amount_ratio.max()), step = 0.1)
    st.markdown("<hr>", unsafe_allow_html=True) 
    
    
    custom_data = pd.DataFrame([{   "account_age_days" : account_age_days,
                                    "total_transactions_user" : total_transactions_user,
                                    "avg_amount_user" : avg_amount_user,
                                    "amount" : amount,
                                    "country" : country,
                                    "bin_country" : bin_country,
                                    "channel" : channel,
                                    "merchant_category" : merchant_category,
                                    "promo_used" : promo_used,
                                    "avs_match" : avs_match,
                                    "cvv_result" : cvv_result,
                                    "three_ds_flag" : three_ds_flag,
                                    "shipping_distance_km" : shipping_distance_km,
                                    "day_of_week" : day_of_week,
                                    "day_of_month" : day_of_month,
                                    "day_period" : day_period,
                                    "amount_ratio" : amount_ratio,
                                    "cross_border" : cross_border,
                                    "security_score" : security_score,
                                    "far_shipping" : far_shipping,
                                    "user_type" : user_type }])
                                
    st.write("✅ New data preview:")
    st.dataframe(custom_data)

    # detect new data 
    data = load_model()
    model = data["model"]
    threshold = data["threshold"]

    predict_button = st.button('Detect Transaction Type', key="predict_btn2")
    if predict_button:
        # Predict probability
        fraud_prob = model.predict_proba(custom_data)[:, 1][0]
        # Apply Threshold
        prediction = int(fraud_prob >= threshold)
        # Display probability
        st.metric(
                  "Fraud Probability",
                  f"{fraud_prob * 100:.2f}%")
        # Display result
        if prediction == 0:
            st.success("🛍️ This Operation is Normal Transaction")
        else:
            st.error("⚠️ This Operation is Fraud Transaction")

def go_to(page):
    st.session_state["fade"] = True
    sleep(0.3)
    st.session_state["current_page"] = page
    
nav1, nav2, nav3 = st.columns([1, 2, 1])
with nav1:
    if st.button("⬅️ Back"):
        go_to("pages\eda.py")
        st.switch_page("pages\eda.py")

with nav3:
    if st.button("➡️ Next"):
        go_to("pages/presentation.py")
        st.switch_page("pages/presentation.py")
