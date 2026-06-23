import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="BikeWale Analytics Dashboard",
    page_icon="🏍️",
    layout="wide"
)

# ======================
# CUSTOM CSS
# ======================
st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 50%,
        #1e1b4b 100%
    );
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0b1120;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Main Title */
h1 {
    color: #ffffff !important;
    text-align: center;
    font-weight: 700;
}

/* Section Headers */
h2, h3 {
    color: #e2e8f0 !important;
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 15px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.25);
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 15px;
}

/* Radio Buttons */
.stRadio > div {
    background: rgba(255,255,255,0.04);
    padding: 10px;
    border-radius: 12px;
}

/* Plot Containers */
.element-container {
    border-radius: 15px;
}

/* Custom Cards */
.insight-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border-radius: 16px;
    padding: 20px;
    color: white;
    margin-bottom: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.25);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #0f172a;
}

::-webkit-scrollbar-thumb {
    background: #6366f1;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ======================
# LOAD DATA
# ======================
df = pd.read_csv("Data/bikewale_bikes.csv")

# Cleaning
df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

df["Engine_CC"] = df["Engine_CC"].astype(str).str.replace(" cc", "")
df["Engine_CC"] = pd.to_numeric(df["Engine_CC"], errors="coerce")

df["Mileage"] = df["Mileage"].astype(str).str.replace(" kmpl", "")
df["Mileage"] = pd.to_numeric(df["Mileage"], errors="coerce")

df["Power_BHP"] = df["Power_BHP"].astype(str).str.replace(" bhp", "")
df["Power_BHP"] = pd.to_numeric(df["Power_BHP"], errors="coerce")

df["Weight_KG"] = df["Weight_KG"].astype(str).str.replace(" kg", "")
df["Weight_KG"] = pd.to_numeric(df["Weight_KG"], errors="coerce")

df["Price"] = df["Price"].astype(str)
df["Price"] = df["Price"].str.replace("₹", "", regex=False)
df["Price"] = df["Price"].str.replace(",", "", regex=False)
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

# ======================
# SIDEBAR
# ======================
st.sidebar.title("Bike Wale-Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Univariate Analysis",
        "Bivariate Analysis",
        "Multivariate Analysis",
        "Insights"
    ]
)

# ======================
# OVERVIEW
# ======================
if page == "Overview":

    st.title("🏍️ BikeWale Analytics Dashboard")
    st.markdown("### Explore Bike Pricing, Ratings, Mileage & Performance")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏍️ Total Bikes", len(df))
    col2.metric("⭐ Avg Rating", round(df["Rating"].mean(), 2))
    col3.metric("💰 Avg Price", f"₹{df['Price'].mean():,.0f}")
    col4.metric("⛽ Avg Mileage", round(df["Mileage"].mean(), 2))

    st.divider()

    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head(10))

# ======================
# UNIVARIATE ANALYSIS
# ======================
elif page == "Univariate Analysis":

    st.header("📊 Univariate Analysis")

    st.subheader("💰 Price Distribution:")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.histplot(df["Price"], kde=True, ax=ax)
    st.pyplot(fig)

    st.subheader("⛽ Mileage Distribution:")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.kdeplot(df["Mileage"], fill=True, ax=ax)
    st.pyplot(fig)

    st.subheader("⭐ Rating Distribution:")
    fig, ax = plt.subplots(figsize=(8,4))
    sns.countplot(x="Rating", data=df, ax=ax)
    st.pyplot(fig)

# ======================
# BIVARIATE ANALYSIS
# ======================
elif page == "Bivariate Analysis":

    st.header("🔍 Bivariate Analysis")

    st.subheader("Engine Capacity vs Mileage:")

    fig, ax = plt.subplots(figsize=(8,4))
    sns.scatterplot(
        data=df,
        x="Engine_CC",
        y="Mileage",
        hue="Price",
        ax=ax
    )
    st.pyplot(fig)

    st.subheader("Top 10 Most Expensive Bikes:")

    top10 = df.groupby("Bike_Name")["Price"].max().reset_index()
    top10 = top10.sort_values("Price", ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(8,4))
    sns.barplot(
        data=top10,
        x="Price",
        y="Bike_Name",
        ax=ax
    )
    st.pyplot(fig)

# ======================
# MULTIVARIATE ANALYSIS
# ======================
elif page == "Multivariate Analysis":

    st.header("🔥 Multivariate Analysis")

    st.subheader("Correlation Heatmap:")

    fig, ax = plt.subplots(figsize=(8,4))

    sns.heatmap(
        df[
            ["Engine_CC","Mileage","Power_BHP","Weight_KG","Price"]
        ].corr(),
        annot=True,
        cmap="coolwarm",
        ax=ax
    )

    st.pyplot(fig)
# ======================
# INSIGHTS
# ======================
elif page == "Insights":

    st.title("📌 Business Insights & Recommendations")

    # Key Insights
    st.markdown("""
    <div style="
    background-color:#1e293b;
    padding:20px;
    border-radius:12px;
    border-left:5px solid #38bdf8;
    color:white;
    margin-bottom:15px;
    ">

    <h2 style="color:white;">📊 Key Insights:</h2>

    • Most bikes receive ratings between <b>4.5 and 4.8</b>, indicating high customer satisfaction.<br>

    • Engine Capacity (CC) has a strong positive relationship with <b>Price</b> and <b>Power</b>.<br>

    • Bikes with higher engine capacity generally offer <b>lower mileage</b>.<br>

    • The market is dominated by <b>commuter and mid-range motorcycles</b>.<br>

    • Premium motorcycles occupy the highest price segment but represent a smaller share of the market.

    </div>
    """, unsafe_allow_html=True)

    # Recommendations
    st.markdown("""
    <div style="
    background-color:#1e293b;
    padding:20px;
    border-radius:12px;
    border-left:5px solid #22c55e;
    color:white;
    margin-bottom:15px;
    ">

    <h2 style="color:white;">💼 Business Recommendations:</h2>

    • Focus on fuel-efficient commuter bikes to target mass-market customers.<br>

    • Introduce performance-oriented models for premium buyers.<br>

    • Improve customer experience and after-sales service to maintain high ratings.<br>

    • Balance performance and mileage to attract a wider audience.<br>

    • Use customer ratings and reviews to guide future product improvements.

    </div>
    """, unsafe_allow_html=True)

    # Conclusion
    st.markdown("""
    <div style="
    background-color:#1e293b;
    padding:20px;
    border-radius:12px;
    border-left:5px solid #f59e0b;
    color:white;
    ">

    <h2 style="color:white;">✅ Conclusion:</h2>

    • Engine Capacity is the primary factor influencing bike <b>Price, Power, Weight, and Mileage</b>.<br>

    • Customers seeking affordability prefer commuter bikes, while enthusiasts prioritize performance and premium features.<br>

    • Manufacturers should maintain a balance between <b>performance, fuel efficiency, and pricing</b> to maximize market reach.

    </div>
    """, unsafe_allow_html=True)