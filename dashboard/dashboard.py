import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Menyiapkan judul dashboard
st.set_page_config(page_title="E-Commerce Dashboard", page_icon="🛒", layout="wide")

# Helper function untuk memuat data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

all_df = load_data()

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("E-Commerce Public Data")
    
    # Menambahkan filter rentang waktu (opsional, untuk menambah nilai interaktif)
    min_date = all_df["order_purchase_timestamp"].min()
    max_date = all_df["order_purchase_timestamp"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memfilter data berdasarkan input dari sidebar
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

# ==============================
# MAIN PAGE
# ==============================
st.title("🛒 E-Commerce Public Dashboard")
st.markdown("##")

# Menampilkan metrik utama (Total Orders, Total Revenue, Total Customers)
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = main_df['order_id'].nunique()
    st.metric("Total Pesanan", value=total_orders)

with col2:
    total_revenue = main_df['price'].sum()
    st.metric("Total Pendapatan", value=f"BRL {total_revenue:,.2f}")

with col3:
    total_customers = main_df['customer_id'].nunique()
    st.metric("Total Pelanggan", value=total_customers)

st.markdown("---")

# ==============================
# VISUALISASI 1: Produk Terbaik dan Terburuk
# ==============================
st.subheader("Kategori Produk Berdasarkan Pendapatan (Top & Bottom)")

revenue_by_category = main_df.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False).reset_index()

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors_main = ["#72BCD4"] + ["#D3D3D3"] * 4 

sns.barplot(x="price", y="product_category_name_english", data=revenue_by_category.head(5), palette=colors_main, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Total Revenue (BRL)")
ax[0].set_title("Top 5 Kategori", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)

sns.barplot(x="price", y="product_category_name_english", data=revenue_by_category.tail(5).sort_values(by="price", ascending=True), palette=colors_main, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Total Revenue (BRL)")
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Bottom 5 Kategori", loc="center", fontsize=15)
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)

st.markdown("---")

# ==============================
# VISUALISASI 2 & 3: Demografi & Tren
# ==============================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Demografi Pelanggan (Top 10 State)")
    bystate_df = main_df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={"customer_id": "customer_count"}, inplace=True)
    bystate_df = bystate_df.sort_values(by="customer_count", ascending=False)

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    colors_state = ["#72BCD4" if i == 0 else "#D3D3D3" for i in range(10)]
    sns.barplot(
        x="customer_count", 
        y="customer_state",
        data=bystate_df.head(10),
        palette=colors_state,
        ax=ax2
    )
    ax2.set_xlabel("Jumlah Pelanggan")
    ax2.set_ylabel("Negara Bagian (State)")
    st.pyplot(fig2)

with col_right:
    st.subheader("Tren Pesanan per Bulan (Tahun 2018)")
    orders_2018 = main_df[main_df['order_purchase_timestamp'].dt.year == 2018].copy()
    
    # Membuat format bulan-tahun secara aman di Pandas/Streamlit
    orders_2018['month_year'] = orders_2018['order_purchase_timestamp'].dt.strftime('%Y-%m')
    monthly_orders = orders_2018.groupby('month_year')['order_id'].nunique().reset_index()

    fig3, ax3 = plt.subplots(figsize=(10, 6))
    ax3.plot(
        monthly_orders['month_year'], 
        monthly_orders['order_id'], 
        marker='o', 
        linewidth=2, 
        color="#72BCD4"
    )
    ax3.set_xlabel("Bulan")
    ax3.set_ylabel("Total Pesanan")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

st.caption("Copyright (c) Bhenarezky Suranta Ginting 2026")