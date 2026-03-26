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
    # Menambahkan try-except agar aman dijalankan di lokal maupun di Streamlit Cloud
    try:
        df = pd.read_csv("dashboard/main_data.csv")
    except FileNotFoundError:
        df = pd.read_csv("main_data.csv")
        
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    
    # Mengekstrak jam dan nama hari untuk visualisasi pola waktu
    df['order_hour'] = df['order_purchase_timestamp'].dt.hour
    df['order_day_name'] = df['order_purchase_timestamp'].dt.day_name()
    return df

all_df = load_data()

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    st.title("E-Commerce Public Data")
    
    # Menambahkan filter rentang waktu
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

# Menampilkan metrik utama
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
colors_top = ["#72BCD4"] + ["#D3D3D3"] * 4 

# Barplot Top 5
sns.barplot(x="price", y="product_category_name_english", data=revenue_by_category.head(5), palette=colors_top, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Total Revenue (BRL)", fontsize=12)
ax[0].set_title("Top 5 Kategori", loc="center", fontsize=15)
ax[0].tick_params(axis ='y', labelsize=12)

# Barplot Bottom 5 (Sudah diperbaiki sorting dan warnanya)
sns.barplot(x="price", y="product_category_name_english", data=revenue_by_category.tail(5).sort_values(by="price", ascending=False), palette=colors_top, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Total Revenue (BRL)", fontsize=12)
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

st.markdown("---")

# ==============================
# VISUALISASI 4: Pola Waktu Transaksi (Jam & Hari)
# ==============================
st.subheader("Pola Waktu Transaksi Pelanggan")
col_time1, col_time2 = st.columns(2)

with col_time1:
    byhour_df = main_df.groupby(by="order_hour").order_id.nunique().reset_index()
    byhour_df.rename(columns={"order_id": "order_count"}, inplace=True)
    
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    top_hour = byhour_df.loc[byhour_df['order_count'].idxmax(), 'order_hour']
    colors_hour = ["#72BCD4" if hour == top_hour else "#D3D3D3" for hour in byhour_df['order_hour']]
    
    sns.barplot(x="order_hour", y="order_count", data=byhour_df, palette=colors_hour, ax=ax4)
    ax4.set_xlabel("Jam (Hour of Day)")
    ax4.set_ylabel("Total Pesanan")
    ax4.set_title("Distribusi Pesanan Berdasarkan Jam", loc="center", fontsize=13)
    st.pyplot(fig4)

with col_time2:
    byday_df = main_df.groupby(by="order_day_name").order_id.nunique().reset_index()
    byday_df.rename(columns={"order_id": "order_count"}, inplace=True)
    
    # Mengurutkan hari
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    byday_df['order_day_name'] = pd.Categorical(byday_df['order_day_name'], categories=days_order, ordered=True)
    byday_df = byday_df.sort_values("order_day_name")
    
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    top_day = byday_df.loc[byday_df['order_count'].idxmax(), 'order_day_name']
    colors_day = ["#72BCD4" if day == top_day else "#D3D3D3" for day in byday_df['order_day_name']]
    
    sns.barplot(x="order_day_name", y="order_count", data=byday_df, palette=colors_day, ax=ax5)
    ax5.set_xlabel("Hari (Day of Week)")
    ax5.set_ylabel("Total Pesanan")
    ax5.set_title("Distribusi Pesanan Berdasarkan Hari", loc="center", fontsize=13)
    plt.xticks(rotation=45)
    st.pyplot(fig5)

st.caption("Copyright (c) Bhenarezky Suranta Ginting 2026")