
import streamlit as st

st.set_page_config(page_title="E-Commerce Fraud Radar", page_icon="🛡️",
                    layout="wide", initial_sidebar_state="collapsed")

# ==========================================
# CSS — unified with presentation.py's theme
# ==========================================
st.markdown("""
<style>
#MainMenu{visibility:hidden;} footer{visibility:hidden;} header{visibility:hidden;}
html,body,[class*="css"]{background:#08111f;color:white;font-family:'Segoe UI',sans-serif;}
.stApp{background:radial-gradient(circle at top,#13213b,#07111f 70%);
animation:fadeEffect .6s;}
@keyframes fadeEffect{from{opacity:0;} to{opacity:1;}}

.title{text-align:center;font-size:48px;font-weight:800;
background:linear-gradient(90deg,#22d3ee,#38bdf8,#2dd4bf);
-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.subtitle{text-align:center;color:#94a3b8;font-size:18px;margin-bottom:10px;}

.hero{position:relative;border-radius:22px;overflow:hidden;height:280px;
margin:20px 0 35px;border:1px solid rgba(255,255,255,.08);}
.hero img{width:100%;height:100%;object-fit:cover;filter:brightness(.55) saturate(1.1);}
.hero-overlay{position:absolute;inset:0;
background:linear-gradient(180deg,rgba(8,17,31,.15) 0%,rgba(8,17,31,.85) 85%),
radial-gradient(circle at 20% 20%,rgba(34,211,238,.25),transparent 55%);
display:flex;align-items:flex-end;padding:24px 32px;}
.hero-overlay h2{margin:0;color:white;font-size:26px;}
.hero-overlay p{margin:4px 0 0;color:#cbd5e1;font-size:15px;}

div.stButton > button{
background:rgba(255,255,255,.05);color:white;border-radius:16px;
border:1px solid rgba(255,255,255,.08);font-weight:700;padding:14px 0;
width:100%;transition:.3s;}
div.stButton > button:hover{
transform:translateY(-4px);border-color:#22d3ee;color:#22d3ee;
box-shadow:0 0 25px rgba(34,211,238,.3);background:rgba(255,255,255,.08);}

.footer{text-align:center;margin-top:40px;color:#64748b;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER
# ==========================================
st.markdown("<div class='title'>🛡️ E-Commerce Fraud Radar</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Analyzing multi-transaction patterns & behavioral signals.</div>",
            unsafe_allow_html=True)

# ==========================================
# HERO IMAGE
# Photo by Petter Lagson on Unsplash — free to use, no attribution required
# https://unsplash.com/photos/black-smartphone-duMttyw2Xc0
# ==========================================
IMG = "https://www.fraud.com/wp-content/uploads/2023/05/E-commerce-fraud-768x401.jpg"

st.markdown(f"""
<div class="hero">
  <img src="{IMG}" alt="Cybersecurity and digital payments">
  <div class="hero-overlay">
    <div>
      <h2>Detecting Fraud Across 299,695 Transactions</h2>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ====================NAVIGATION======================
col1, col2, col3, col4 = st.columns(4, gap="large")
 
with col1:
    if st.button("ℹ️ About"):
        st.switch_page("pages/about.py")
 
with col2:
    if st.button("📊 EDA"):
        st.switch_page("pages/eda.py")
 
with col3:
    if st.button("🤖 Modeling"):
        st.switch_page("pages/modeling.py")
 
with col4:
    if st.button("📈 Presentation"):
        st.switch_page("pages/presentation.py")

st.markdown(""" <div class="footer"><br>
<h2>🛡 E-Commerce Fraud Detection</h2><br>
</div> """, unsafe_allow_html=True)

