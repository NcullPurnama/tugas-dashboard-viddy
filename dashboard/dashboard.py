import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
hour_path = "dashboard/hour_fix.csv"
day_path = "dashboard/day_fix.csv"

# Fungsi untuk membaca data
@st.cache_data
def load_data():
    hour_df = pd.read_csv(hour_path, parse_dates=["dteday"])
    day_df = pd.read_csv(day_path, parse_dates=["dteday"])
    return hour_df, day_df

hour_data, day_data = load_data()

# Sidebar: Filter berdasarkan rentang tanggal
st.sidebar.header("Filter Tanggal")
start_date = st.sidebar.date_input("Mulai", day_data["dteday"].min())
end_date = st.sidebar.date_input("Selesai", day_data["dteday"].max())

# Filter data sesuai tanggal
filtered_day_data = day_data[(day_data["dteday"] >= pd.to_datetime(start_date)) &
                             (day_data["dteday"] <= pd.to_datetime(end_date))]

# Halaman utama
st.title("Dashboard Analisis Data Bike Sharing")

# Pertanyaan Bisnis 1: Bagaimana tren jumlah peminjaman sepeda dalam beberapa bulan terakhir?
st.subheader("Tren Jumlah Peminjaman Sepeda Per Bulan")
filtered_day_data["month"] = filtered_day_data["dteday"].dt.to_period("M")
monthly_trend = filtered_day_data.groupby("month")["cnt"].sum().reset_index()
monthly_trend["month"] = monthly_trend["month"].astype(str)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_trend["month"], monthly_trend["cnt"], marker="o", linestyle="-", color="b")
ax.set_title("Tren Jumlah Peminjaman Sepeda Per Bulan")
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Peminjaman")
ax.tick_params(axis='x', rotation=45)
ax.grid(True)
st.pyplot(fig)

st.write("### Analisis:")
st.write("Tren jumlah peminjaman sepeda cenderung meningkat pada bulan-bulan tertentu, terutama saat cuaca lebih mendukung untuk bersepeda.")

# Pertanyaan Bisnis 2: Bagaimana perbedaan jumlah penyewaan sepeda pada hari kerja dan hari libur?
st.subheader("Perbedaan Penyewaan Sepeda pada Hari Kerja dan Hari Libur")
holiday_trend = filtered_day_data.groupby("workingday")["cnt"].sum().reset_index()
holiday_trend["workingday"] = holiday_trend["workingday"].map({0: "Libur", 1: "Hari Kerja"})

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=holiday_trend["workingday"], y=holiday_trend["cnt"], palette=["orange", "gray"], ax=ax)
ax.set_title("Jumlah Penyewaan Sepeda pada Hari Kerja dan Hari Libur")
ax.set_xlabel("Jenis Hari")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

st.write("### Analisis:")
st.write("Peminjaman sepeda lebih banyak terjadi pada hari libur dibandingkan hari kerja, kemungkinan besar karena lebih banyak waktu luang untuk rekreasi.")

# Pertanyaan Bisnis 3: Pada musim mana peminjaman sepeda paling banyak terjadi?
st.subheader("Peminjaman Sepeda Berdasarkan Musim")
season_trend = day_data.groupby("season")["cnt"].sum().reset_index()
season_trend["season"] = season_trend["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=season_trend["season"], y=season_trend["cnt"], palette="Blues", ax=ax)
ax.set_title("Total Peminjaman Sepeda Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

st.write("### Analisis:")
st.write("Musim gugur dan musim panas memiliki jumlah peminjaman sepeda yang lebih tinggi, sementara musim dingin memiliki jumlah peminjaman yang lebih rendah.")

# Pertanyaan Bisnis 4: Apakah suhu mempengaruhi jumlah penyewaan sepeda?
st.subheader("Pengaruh Suhu terhadap Penyewaan Sepeda")

def categorize_temp(temp):
    if temp < 0.3:
        return "Dingin"
    elif temp < 0.6:
        return "Hangat"
    else:
        return "Panas"

day_data["temp_category"] = day_data["temp"].apply(categorize_temp)
temp_trend = day_data.groupby("temp_category")["cnt"].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=temp_trend["temp_category"], y=temp_trend["cnt"], palette="coolwarm", ax=ax)
ax.set_title("Total Penyewaan Sepeda Berdasarkan Suhu")
ax.set_xlabel("Kategori Suhu")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

st.write("### Analisis:")
st.write("Peminjaman sepeda meningkat pada suhu yang lebih hangat, sementara saat suhu sangat dingin, peminjaman cenderung menurun.")
