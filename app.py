import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="MallQ - Shop with High IQ",
    page_icon="🛍️",
    layout="wide"
)

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/products.csv")

df = load_data()

# ---------------------------
# Header
# ---------------------------
st.title("🛍️ MallQ")
st.subheader("Shop with High IQ")

st.markdown("""
### Smart Mall Shopping Assistant

Find products instantly, compare prices, check sizes,
discover discounts, and navigate stores efficiently.
""")

# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("MallQ Menu")

menu = st.sidebar.radio(
    "Choose Feature",
    [
        "Home",
        "Product Search",
        "Price Comparison",
        "Best Deals",
        "Store Locator",
        "Analytics"
    ]
)

# ---------------------------
# HOME
# ---------------------------
if menu == "Home":

    st.image(
        "https://images.unsplash.com/photo-1519567241046-7f570eee3ce6",
        use_container_width=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Stores Connected", "150+")

    with col2:
        st.metric("Products Indexed", "50,000+")

    with col3:
        st.metric("Avg. Time Saved", "40%")

    st.markdown("---")

    st.info(
        "MallQ helps shoppers locate products, verify availability, compare prices, and discover discounts in real-time."
    )

# ---------------------------
# PRODUCT SEARCH
# ---------------------------
elif menu == "Product Search":

    st.header("🔍 Product Search")

    product_name = st.text_input(
        "Search Product"
    )

    selected_size = st.selectbox(
        "Select Size",
        ["Any"] + list(df["Size"].astype(str).unique())
    )

    filtered = df.copy()

    if product_name:
        filtered = filtered[
            filtered["Product"]
            .str.contains(product_name, case=False)
        ]

    if selected_size != "Any":
        filtered = filtered[
            filtered["Size"].astype(str) == selected_size
        ]

    st.dataframe(filtered)

    if len(filtered) > 0:

        st.success(
            f"{len(filtered)} matching products found."
        )

# ---------------------------
# PRICE COMPARISON
# ---------------------------
elif menu == "Price Comparison":

    st.header("💰 Price Comparison")

    product_list = df["Product"].unique()

    selected_product = st.selectbox(
        "Select Product",
        product_list
    )

    compare_df = df[
        df["Product"] == selected_product
    ]

    st.dataframe(compare_df)

    fig = px.bar(
        compare_df,
        x="Store",
        y="Price",
        color="Discount",
        title=f"Price Comparison for {selected_product}"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# BEST DEALS
# ---------------------------
elif menu == "Best Deals":

    st.header("🔥 Today's Best Deals")

    deals = df.sort_values(
        by="Discount",
        ascending=False
    )

    st.dataframe(deals)

    top_deals = deals.head(5)

    fig = px.pie(
        top_deals,
        names="Product",
        values="Discount",
        title="Top Discounted Products"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------
# STORE LOCATOR
# ---------------------------
elif menu == "Store Locator":

    st.header("📍 Store Locator")

    stores = df["Store"].unique()

    selected_store = st.selectbox(
        "Choose Store",
        stores
    )

    store_data = df[
        df["Store"] == selected_store
    ]

    floor = store_data["Floor"].iloc[0]

    st.success(
        f"{selected_store} is located on {floor} Floor"
    )

    st.markdown("### Navigation")

    mall_map = {
        "Ground":
        "Entrance → Straight 50m → Left Wing",

        "First":
        "Escalator → First Floor → Right Wing",

        "Second":
        "Escalator → Second Floor → Fashion Zone"
    }

    st.info(mall_map[floor])

# ---------------------------
# ANALYTICS
# ---------------------------
elif menu == "Analytics":

    st.header("📊 Mall Insights")

    store_count = (
        df.groupby("Store")
        .size()
        .reset_index(name="Products")
    )

    fig = px.bar(
        store_count,
        x="Store",
        y="Products",
        title="Products Available per Store"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    discount_fig = px.histogram(
        df,
        x="Discount",
        title="Discount Distribution"
    )

    st.plotly_chart(
        discount_fig,
        use_container_width=True
    )

st.markdown("---")
st.caption("MallQ © 2026 | Shop with High IQ")