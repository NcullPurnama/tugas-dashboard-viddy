import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
orders_path = "../data/orders_dataset.csv"
customers_path = "../data/customers_dataset.csv"
order_items_path = "../data/order_items_dataset.csv"
products_path = "../data/products_dataset.csv"
reviews_path = "../data/order_reviews_dataset.csv"
sellers_path = "../data/sellers_dataset.csv"

# Fungsi untuk membaca data
@st.cache_data
def load_data():
    orders_df = pd.read_csv(orders_path, parse_dates=["order_purchase_timestamp", "order_delivered_customer_date"])
    customers_df = pd.read_csv(customers_path)
    order_items_df = pd.read_csv(order_items_path)
    products_df = pd.read_csv(products_path)
    reviews_df = pd.read_csv(reviews_path)
    sellers_df = pd.read_csv(sellers_path)
    
    # Gabungkan data
    orders_customers_df = orders_df.merge(customers_df, on="customer_id", how="left")
    orders_customers_df["delivery_time"] = (orders_customers_df["order_delivered_customer_date"] - orders_customers_df["order_purchase_timestamp"]).dt.days
    
    order_items_products_df = order_items_df.merge(products_df, on="product_id", how="left")
    
    return orders_customers_df, order_items_products_df, reviews_df, sellers_df

data_orders, data_order_items, data_reviews, data_sellers = load_data()

# Sidebar: Filter berdasarkan rentang tanggal
st.sidebar.header("Filter Tanggal")
start_date = st.sidebar.date_input("Mulai", data_orders["order_purchase_timestamp"].min())
end_date = st.sidebar.date_input("Selesai", data_orders["order_purchase_timestamp"].max())

# Filter data sesuai tanggal
filtered_orders = data_orders[(data_orders["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
                              (data_orders["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

# Halaman utama
st.title("Dashboard Analisis E-Commerce")

# 1. Tren jumlah pesanan per bulan
st.subheader("Tren Jumlah Pesanan Per Bulan")
orders_trend = filtered_orders.groupby(filtered_orders["order_purchase_timestamp"].dt.to_period("M")).size().reset_index(name="total_orders")
orders_trend["order_purchase_timestamp"] = orders_trend["order_purchase_timestamp"].astype(str)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(orders_trend["order_purchase_timestamp"], orders_trend["total_orders"], marker="o", linestyle="-", color="b")
ax.set_title("Tren Jumlah Pesanan Per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Pesanan")
ax.tick_params(axis='x', rotation=45)
ax.grid(True)
st.pyplot(fig)

# 2. Waktu pengiriman berdasarkan kota
st.subheader("Rata-rata Waktu Pengiriman Berdasarkan Kota")
delivery_time_per_city = filtered_orders.groupby("customer_city")["delivery_time"].mean().reset_index()
delivery_time_per_city = delivery_time_per_city.sort_values(by="delivery_time", ascending=False).head(20)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(y=delivery_time_per_city["customer_city"], x=delivery_time_per_city["delivery_time"], palette="Blues_r", ax=ax)
ax.set_title("Top 20 Kota dengan Rata-rata Waktu Pengiriman Tertinggi")
ax.set_xlabel("Rata-rata Waktu Pengiriman (hari)")
ax.set_ylabel("Kota")
ax.grid(axis="x", linestyle="--", alpha=0.7)
st.pyplot(fig)

# 3. Kategori produk paling banyak dibeli
st.subheader("Kategori Produk Paling Banyak Dibeli")
product_counts = data_order_items["product_category_name"].value_counts().head(10)
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=product_counts.values, y=product_counts.index, palette="viridis", ax=ax)
ax.set_title("Top 10 Kategori Produk")
ax.set_xlabel("Jumlah Pembelian")
ax.set_ylabel("Kategori Produk")
st.pyplot(fig)

# 4. Distribusi rating ulasan pelanggan
st.subheader("Distribusi Rating Ulasan")
rating_counts = data_reviews["review_score"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(7, 5))
sns.barplot(x=rating_counts.index, y=rating_counts.values, palette="coolwarm", ax=ax)
ax.set_title("Distribusi Rating Ulasan Pelanggan")
ax.set_xlabel("Rating")
ax.set_ylabel("Jumlah Ulasan")
st.pyplot(fig)

# 5. Penjual dengan jumlah produk terbanyak
st.subheader("Penjual dengan Produk Terbanyak")
seller_product_counts = data_order_items.groupby("seller_id").size().reset_index(name="total_products")
seller_product_counts = seller_product_counts.sort_values(by="total_products", ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x=seller_product_counts["total_products"], y=seller_product_counts["seller_id"], palette="magma", ax=ax)
ax.set_title("Top 10 Penjual dengan Produk Terbanyak")
ax.set_xlabel("Jumlah Produk")
ax.set_ylabel("ID Penjual")
st.pyplot(fig)
