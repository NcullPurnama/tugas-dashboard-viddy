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

# Fungsi untuk menyaring data antara tahun 2011-2012
def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query('dteday >= "2011-01-01" and dteday < "2012-12-31"')
    return day_df_count_2011

min_date = day_data["dteday"].min()
max_date = day_data["dteday"].max()

default_start_date = pd.to_datetime("2011-01-01")
default_end_date = pd.to_datetime("2012-01-01")

# Sidebar: Filter berdasarkan rentang tanggal
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[default_start_date, default_end_date]
    )

# Filter data sesuai tanggal
filtered_day_data = day_data[(day_data["dteday"] >= pd.to_datetime(start_date)) &
                             (day_data["dteday"] <= pd.to_datetime(end_date))]
filtered_hour_data = hour_data[(hour_data["dteday"] >= pd.to_datetime(start_date)) &
                               (hour_data["dteday"] <= pd.to_datetime(end_date))]

main_df = filtered_day_data.copy()
second_df = filtered_hour_data.copy()

# Halaman utama
st.title("Dashboard Analisis Data Bike Sharing")

# Pertanyaan Bisnis 1: Bagaimana tren jumlah peminjaman sepeda dalam beberapa bulan terakhir?
st.subheader("Tren Jumlah Peminjaman Sepeda dalam beberapa bulan terakhir")
main_df["day"] = main_df["dteday"].dt.to_period("D")  # Ubah ke periode harian
daily_trend = main_df.groupby("day")["cnt"].sum().reset_index()
daily_trend["day"] = daily_trend["day"].astype(str)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(daily_trend["day"], daily_trend["cnt"], marker="o", linestyle="-", color="b")
ax.set_title("Tren Jumlah Peminjaman Sepeda Per Hari")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Total Peminjaman")
ax.tick_params(axis='x', rotation=45)
ax.grid(True)
st.pyplot(fig)

st.write("### Analisis:")
st.write("Data yang ditampilkan sesuai dengan rentang waktu yang dipilih di sidebar. Tren peminjaman sepeda dapat berbeda tergantung pada hari dan kebiasaan pengguna dalam periode tersebut.")

# Pertanyaan Bisnis 2: Bagaimana perbedaan jumlah penyewaan sepeda pada hari kerja dan hari libur?
st.subheader("Perbedaan Penyewaan Sepeda pada Hari Kerja dan Hari Libur")
holiday_trend = main_df.groupby("workingday")["cnt"].sum().reset_index()
holiday_trend["workingday"] = holiday_trend["workingday"].map({0: "Libur", 1: "Hari Kerja"})

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=holiday_trend["workingday"], y=holiday_trend["cnt"], palette=["orange", "gray"], ax=ax)
ax.set_title("Jumlah Penyewaan Sepeda pada Hari Kerja dan Hari Libur")
ax.set_xlabel("Jenis Hari")
ax.set_ylabel("Total Penyewaan")
st.pyplot(fig)

st.write("### Analisis:")
st.write("Grafik ini memperlihatkan perbedaan jumlah penyewaan sepeda berdasarkan hari kerja dan hari libur sesuai rentang waktu yang dipilih.")