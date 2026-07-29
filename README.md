# 🛡️ E-Commerce Fraud Detection

**An end-to-end Machine Learning pipeline for detecting fraudulent e-commerce transactions**, built on 299,695 real transactions across 10 countries. The final CatBoost model achieves a **97.62% ROC AUC**, catching 81% of fraud at 84% precision.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![CatBoost](https://img.shields.io/badge/Model-CatBoost-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Results](#-key-results)
- [Dataset](#-dataset)
- [Project Workflow](#-project-workflow)
- [Feature Engineering](#-feature-engineering)
- [Exploratory Data Analysis — Key Insights](#-exploratory-data-analysis--key-insights)
- [Modeling & Comparison](#-modeling--comparison)
- [Final Model & Threshold Optimization](#-final-model--threshold-optimization)
- [Streamlit App](#-streamlit-app)
- [Project Structure](#-project-structure)
- [Installation & Usage](#-installation--usage)
- [Tech Stack](#-tech-stack)
- [Future Work](#-future-work)
- [Author](#-author)

---

## 📖 Overview

Online payment platforms process thousands of transactions per day, making manual fraud review impractical. This project builds a complete ML pipeline — from data cleaning and feature engineering to model selection and decision-threshold tuning — to automatically flag fraudulent transactions while minimizing disruption to legitimate customers, on a dataset where fraud represents only **~2%** of all activity.

**Objectives:**
- Analyze transaction patterns and customer behavior.
- Engineer features that capture real fraud signals (geography, shipping, customer tenure).
- Train and compare multiple classification models.
- Optimize the decision threshold based on the precision/recall trade-off.
- Ship an interactive Streamlit app to explore the results.

---

## 🏆 Key Results

| Metric | Score |
|---|---|
| **Best Model** | CatBoost + SMOTE |
| **ROC AUC** | 97.62% |
| **Precision** | 84% |
| **Recall** | 81% |
| **F1 Score** | 82% |
| **Transactions Analyzed** | 299,695 |
| **Countries Covered** | 10 |

---

## 🗂 Dataset

- **299,695 transactions**, originally 17 columns, **zero duplicates and zero missing values**.
- **10 countries**: France, US, Turkey, Poland, Spain, Italy, Romania, UK, Netherlands, Germany.
- **5 merchant categories**: electronics, fashion, gaming, travel, grocery.
- **Payment channels**: Web / App.
- **Risk signals**: 3D-Secure flag, AVS match, CVV result, promo usage.
- **Customer profile**: account age, transaction history, average historical spend.
- **Target**: binary fraud label, highly imbalanced (~2% positive class).

---

## 🔄 Project Workflow

```
📂 Raw Data (299,695 rows)
        ⬇
🧹 Cleaning & Time Parsing
        ⬇
⚙️ Feature Engineering
        ⬇
🔄 RobustScaler / Binary Encoding / One-Hot Encoding
        ⬇
⚖️ SMOTE (class balancing)
        ⬇
🤖 Model Training & Comparison
        ⬇
🎯 Hyperparameter Tuning (CatBoost)
        ⬇
📈 Threshold Optimization
        ⬇
🖥️ Streamlit App
```

---

## 🔧 Feature Engineering

| Feature | Description |
|---|---|
| `amount_ratio` | Transaction amount ÷ customer's average historical spend |
| `cross_border` | Flag for transaction country ≠ card-issuing country |
| `far_shipping` | Flag for shipping distance > 500 km |
| `security_score` | Combined AVS match + 3D-Secure flag |
| `user_type` | new / regular / old, derived from account age |
| `day_period`, `day_of_week`, `day_of_month` | Extracted from the raw transaction timestamp |

**Encoding & Scaling:**
- `RobustScaler` on numeric features — resistant to the extreme outliers deliberately kept in amount and shipping distance.
- `BinaryEncoder` for high-cardinality country features (10 categories each).
- `OneHotEncoder` for channel, merchant category, day-of-week, day-period, and user type.

---

## 📊 Exploratory Data Analysis — Key Insights

| Insight | Finding |
|---|---|
| 🌐 **Channel matters** | Web fraud rate **3.56%** vs App **0.80%** (χ² p < 0.001) |
| ✈️ **Cross-border risk** | **11.28%** fraud rate vs **1.43%** domestic — ~8× higher |
| 📦 **Shipping distance** | `far_shipping` (>500km): **15.89%** fraud vs **0.96%** — the strongest single signal, ~16× higher |
| 👤 **New customers** | **17%** fraud rate vs **~1%** for regular/old users |
| 🌍 **Country risk** | Turkey highest exposure (~2.8%), Romania elevated, Germany lowest (~1.7%) |
| 🕐 **Time of day** | No statistically significant effect (χ² p = 0.45) |
| 💰 **Transaction amount** | Fraudulent transactions run **~3.5× larger** on average than legitimate ones across every merchant category |

These findings directly motivated the `cross_border`, `far_shipping`, `amount_ratio`, and `user_type` engineered features.

---

## 🧪 Modeling & Comparison

Five algorithms were trained and evaluated both with and without SMOTE oversampling:

**F1 Score — Without SMOTE**

| Model | Train | Test |
|---|---|---|
| Logistic Regression | 70.48% | 70.31% |
| Random Forest | 99.98% | 83.81% |
| XGBoost | 90.48% | 81.58% |
| **CatBoost** | 92.46% | 83.17% |
| LightGBM | 84.81% | 80.55% |

**F1 Score — With SMOTE**

| Model | Train | Test |
|---|---|---|
| Logistic Regression | 33.71% | 33.51% |
| Random Forest | 99.99% | 80.68% |
| XGBoost | 88.49% | 83.25% |
| **CatBoost** | 87.23% | **83.52%** |
| LightGBM | 84.40% | 82.92% |

**Why CatBoost:** it delivered the best and most stable test F1 in both setups, handles categorical features and outliers natively, and generalized far better than Random Forest (which overfit to ~100% train F1). CatBoost + SMOTE was selected for hyperparameter tuning.

**Tuning (RandomizedSearchCV):**

| Config | Value |
|---|---|
| `learning_rate` | 0.05 |
| `iterations` | 1000 |
| `depth` | 6 |
| Train F1 | 85.99% |
| Validation F1 | **83.72%** |

An alternative using class weights (`scale_pos_weight=44`) instead of SMOTE was also tested — it reached 91.17% train F1 but only 76.92% validation F1, a clear sign of overfitting, confirming SMOTE as the better generalization strategy.

---

## 🎯 Final Model & Threshold Optimization

| | Threshold 0.50 (default) | Threshold 0.25 (tuned) |
|---|---|---|
| Precision | 96% | 84% |
| Recall | 76% | 81% |
| Fraud Caught | 1,009 / 1,322 | 1,074 / 1,322 |
| False Alarms | 57 | 209 |

Lowering the classification threshold from 0.50 to 0.25 catches **65 additional fraud cases** at a manageable rise in false positives — a trade-off tunable to a business's real fraud-review capacity.

**Top predictive features:** `far_shipping`, `amount_ratio`, `promo_used`, `channel=web`, `account_age_days`, `day_period=Night`, `merchant_category=gaming` — matching the signals uncovered during EDA.

---

## 🖥️ Streamlit App

An interactive multi-page Streamlit app is included to explore the project:

| Page | Description |
|---|---|
| 🏠 Home | Project landing page with navigation |
| ℹ️ About | Project background and objectives |
| 📊 EDA | Interactive exploration of fraud patterns |
| 🤖 Modeling | Model comparison and tuning results |
| 📈 Presentation | Slide-style walkthrough of the full project |

---

## 📁 Project Structure

```
fraud-detection/
│
├── home_page.py                # Streamlit entry point
├── pages/
│   ├── about.py
│   ├── eda.py
│   ├── modeling.py
│   └── presentation.py
│
├── notebooks/
│   └── Fraud_Detection_Project.ipynb   # Full analysis: EDA, feature engineering, modeling
│
├── models/                     # Saved trained model (e.g. catboost_model.pkl)
├── data/                       # Raw / processed dataset (not tracked in Git)
├── requirements.txt
└── README.md
```

> Adjust this tree to match your actual repository layout before publishing.

---

## ⚙️ Installation & Usage

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/fraud-detection.git
cd fraud-detection

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Streamlit app
streamlit run home_page.py
```

**Suggested `requirements.txt`:**
```
streamlit
pandas
numpy
scikit-learn
catboost
xgboost
lightgbm
imbalanced-learn
category_encoders
matplotlib
seaborn
plotly
```

---

## 🛠 Tech Stack

`Python` · `Pandas` · `NumPy` · `Scikit-learn` · `CatBoost` · `XGBoost` · `LightGBM` · `imbalanced-learn (SMOTE)` · `category_encoders` · `Matplotlib` / `Seaborn` / `Plotly` · `Streamlit`

---

## 🚀 Future Work

- Compare outlier-handling strategies (e.g. Winsorization) against the current "keep outliers" approach.
- Evaluate Ordinal Encoding for `user_type`, since it has a natural order (new → regular → old).
- Explore additional class-weight configurations alongside SMOTE.
- Select the final decision threshold based on real business review costs rather than F1 alone.
- Add model explainability (SHAP) to support fraud-analyst decision-making.
- Package the model behind a REST API for real-time scoring.

---

## 👤 Author

**Samir Masoud**

If you found this project useful, consider giving it a ⭐ on GitHub!
