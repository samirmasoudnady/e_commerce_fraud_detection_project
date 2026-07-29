
import streamlit as st
from ydata_profiling import ProfileReport
import matplotlib.pyplot as plt
import plotly.express as px 
from time import sleep
import seaborn as sns
import pandas as pd
import numpy as np

df = pd.read_csv('cleaned_df.csv')
# ========== PAGE TITLE ==========
st.markdown("""<h2 style='text-align:center;color:#00E5FF;'>📊 Exploratory Data Analysis(EDA)</h2>""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ========== BASIC INFO ==========
col1, col2, col3 = st.columns(3)
col1.metric("📈 Numeric Features", f"{len(df.select_dtypes(include= 'number').columns)}")
col2.metric("💳 Num OF Transactions", f"{len(df):,}")
col3.metric("📊 Categorical Features", f"{len(df.select_dtypes(include= 'object').columns)}")


st.markdown("<hr>", unsafe_allow_html=True)

tab_1, tab_2, tab_3 = st.tabs(["📊 Univariate Analysis", "📈 Bivariate Analysis", "📉 Multivariate Analysis"])

with tab_1:
   
    st.markdown("<style> .center-div1 {color: red; text-align: left;} </style> <div class='center-div1'>1.What is the Rate Of fraud Transaction in the dataset?</div>", unsafe_allow_html=True)
    fig1 = px.pie(df, names='is_fraud', title='Fraud Rate', hole=0.5)
    st.plotly_chart(fig1)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<style> .center-div1 {color: red; text-align: left;} </style> <div class='center-div1'>2.What is The Distrabution of all Numrical Columns?</div>", unsafe_allow_html=True)
    num_cols = df.select_dtypes(include= 'number')
    column = st.selectbox("Select Numerical Feature", num_cols.columns)
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))
    sns.histplot(df[column], kde=True, ax=axes[0])
    sns.boxplot(x=df[column], ax=axes[1])
    st.pyplot(fig)
    plt.close(fig)
    st.markdown("<hr>", unsafe_allow_html=True)

with tab_2:
    
    st.markdown("<style> .center-div1 {color: red; text-align: left;} </style> <div class='center-div1'>1.Which numerical features are most strongly correlated with fraudulent transactions?</div>", unsafe_allow_html=True)
    df["binary_fraud"] = df["is_fraud"].map({"Normal" : 0, "Fraud" : 1})
    corr_df = df.corr(numeric_only=True)['binary_fraud'].drop('binary_fraud').sort_values(ascending=False).reset_index()
    corr_df.columns = ['Feature', 'Correlation Coefficient']
    fig_1 = px.bar( data_frame=corr_df, x='Feature', y='Correlation Coefficient', color='Feature', labels={'Feature': 'Feature', 'Correlation Coefficient': 'Correlation Coefficient'})
    st.plotly_chart(fig_1)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<style> .center-div1 {color: red; text-align: left;} </style> <div class='center-div1'>2.Which payment channel has the highest fraud rate?</div>", unsafe_allow_html=True)
    channel_df = round(df.groupby('channel')['is_fraud'].value_counts(normalize=True)*100, 2).sort_values(ascending=False).reset_index()
    fig_2 = px.bar(data_frame= channel_df, x='channel', y='proportion', color='is_fraud', barmode='group', text_auto=True, title='payment channel has the highest fraud rate')
    st.plotly_chart(fig_2)  
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<style> .center-div1 {color: red; text-align: left;} </style> <div class='center-div1'>3.Which countries have the highest Fraud Rate?</div>", unsafe_allow_html=True)
    country_df = round(df.groupby('country')['is_fraud'].value_counts(normalize=True), 3).sort_values(ascending=False).reset_index()
    fig_3 =px.bar(data_frame= country_df, x='country', y='proportion', color='is_fraud', barmode='group', text_auto=True, title='countries have the highest fraud rate')
    st.plotly_chart(fig_3)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<style> .center-div1 {color: red; text-align: left;} </style> <div class='center-div1'>4.Which merchant categories show the highest average transaction amount in fraudulent transactions?</div>", unsafe_allow_html=True)
    cat_df = round(df.groupby(['merchant_category', 'is_fraud'])['amount'].mean(), 2).sort_values(ascending=False).reset_index()
    fig_4 =px.bar(data_frame=cat_df, x='merchant_category', y='amount', color='is_fraud', barmode='group', text_auto=True, title='Influence Transaction Amount by Merchant Category')
    st.plotly_chart(fig_4)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<style> .center-div1 {color: red; text-align: left;} </style> <div class='center-div1'>5.Does spending significantly above a customer's average increase fraud risk?</div>", unsafe_allow_html=True)
    non_outliers = df[df['amount_ratio'] < 3]
    fig_5 = px.box(non_outliers, x="amount_ratio", y="is_fraud", color="is_fraud")
    st.plotly_chart(fig_5)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<style> .center-div1 {color: red; text-align: left;} </style> <div class='center-div1'>6.Are cross-border transactions more likely to be fraudulent?</div>", unsafe_allow_html=True)
    fig_6 = px.histogram(df, x="cross_border", color="is_fraud", barmode="group", text_auto=True)
    st.plotly_chart(fig_6)
    st.markdown("""<div class='subheader'>Transaction Outside The Home County Almost is Fraud Transaction.</div> """, unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<style> .center-div1 {color: red; text-align: left;} </style> <div class='center-div1'>7.Does long-distance shipping increase the likelihood of fraud?</div>", unsafe_allow_html=True)
    fig_7 =px.histogram( df, x="far_shipping", color="is_fraud", barmode="group", text_auto=True)
    st.plotly_chart(fig_7)
    st.markdown("<hr>", unsafe_allow_html=True)    

with tab_3:

    st.markdown("<style> .center-div1 {color: red; text-align: left;} </style> <div class='center-div1'>1.Are newly registered users more vulnerable to fraudulent transactions?</div>", unsafe_allow_html=True)
    fraud_rate = round(df.groupby("user_type")["is_fraud"].value_counts(normalize=True).rename("percentage").reset_index(), 2)
    fig_8 = px.bar( fraud_rate, x="user_type", y="percentage", color="is_fraud", barmode="group", title="Fraud Rate by User Type", text_auto=True)
    st.plotly_chart(fig_8)
    st.markdown("<div class='subheader'>Recently registered customers experience a higher fraud rate than long-term users</div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<style> .center-div1 {color: red; text-align: left;} </style> <div class='center-div1'>2.Which combination of payment channel, user type, and country has the highest fraud rate?</div>", unsafe_allow_html=True)
    fraud_df = (df[df["is_fraud"] == "Fraud"].groupby(["channel", "user_type", "country"]).size().reset_index(name="fraud_count").sort_values("fraud_count", ascending=False).head(15))
    fig_9 = px.bar( fraud_df, x="country", y="fraud_count", color="channel", facet_col="user_type", text_auto=True, 
                   title="Top Channel, User Type and Country Combinations with Highest Fraud Count")
    st.plotly_chart(fig_9)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<style> .center-div1 {color: red; text-align: left;} </style> <div class='center-div1'>3. Are new users making cross-border purchases with long shipping distances more likely to commit fraud?</div>", unsafe_allow_html=True)
    fraud_df1 = df.groupby(["user_type", "cross_border", "far_shipping"])["is_fraud"].value_counts(normalize=True).rename("fraud_rate").reset_index()
    fraud_df1 = fraud_df1[fraud_df1["is_fraud"] == "Fraud"]
    fig_10 = px.bar( fraud_df1, x="user_type", y="fraud_rate", color="cross_border", facet_col="far_shipping", 
                    barmode="group", text_auto=".1%", title="Fraud Rate by User Type, Cross-Border and Shipping Distance")
    st.plotly_chart(fig_10, use_container_width=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    security_df = (df.groupby(["three_ds_flag", "avs_match", "cvv_result"])["is_fraud"].value_counts(normalize=True).rename("fraud_rate").reset_index())
    security_df = security_df[security_df["is_fraud"] == "Fraud"]
    fig_11 = px.bar( security_df, x="three_ds_flag", y="fraud_rate", color="avs_match", facet_col="cvv_result", barmode="group", text_auto=".1%",
             labels={  "three_ds_flag": "3DS Authentication",
                        "avs_match": "AVS Match",
                        "cvv_result": "CVV Result",
                        "fraud_rate": "Fraud Rate" },title="Impact of 3DS, AVS and CVV on Fraud Rate")
    st.plotly_chart(fig_11, use_container_width=True)
    st.markdown("<hr>", unsafe_allow_html=True)

def go_to(page):
    st.session_state["fade"] = True
    sleep(0.3)
    st.session_state["current_page"] = page
    
nav1, nav2, nav3 = st.columns([1, 2, 1])
with nav1:
    if st.button("⬅️ Back"):
        go_to("pages/about.py")
        st.switch_page("pages/about.py")

with nav3:
    if st.button("➡️ Next"):
        go_to("pages\modeling.py")
        st.switch_page("pages\modeling.py")
