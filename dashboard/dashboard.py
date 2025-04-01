import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
hour_path = "hour_fix.csv"
day_path = "day_fix.csv"

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
default_end_date = pd.to_datetime("2011-01-31")

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

# Pertanyaan Bisnis 1: Pada jam berapa penyewaan sepeda mencapai puncaknya dan kapan terjadi penurunan paling signifikan pada hari kerja dan hari libur?
st.subheader("Tren Penyewaan Sepeda Berdasarkan Jam")

# Mengelompokkan data berdasarkan jam dan hari kerja
hourly_trend = second_df.groupby(['hr', 'workingday'])['cnt'].sum().reset_index()

# Mengubah nilai 'workingday' menjadi label yang lebih mudah dibaca
hourly_trend['workingday'] = hourly_trend['workingday'].map({0: "Libur", 1: "Hari Kerja"})

# Membuat grafik
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hourly_trend, x='hr', y='cnt', hue='workingday', marker='o', ax=ax)
ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Jam (Hari Kerja vs Hari Libur)")
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
plt.xticks(range(0, 24))  # Menampilkan jam dari 0 hingga 23
st.pyplot(fig)

# Menemukan jam puncak dan penurunan signifikan
peak_hour_workday = hourly_trend.loc[(hourly_trend['workingday'] == "Hari Kerja") & (hourly_trend['cnt'] == hourly_trend[hourly_trend['workingday'] == "Hari Kerja"]['cnt'].max())]
significant_drop_hour_workday = hourly_trend.loc[(hourly_trend['workingday'] == "Hari Kerja")].copy()
significant_drop_hour_workday['drop'] = significant_drop_hour_workday['cnt'].diff()
significant_drop_hour_workday = significant_drop_hour_workday.loc[significant_drop_hour_workday['drop'].idxmin()]

peak_hour_holiday = hourly_trend.loc[(hourly_trend['workingday'] == "Libur") & (hourly_trend['cnt'] == hourly_trend[hourly_trend['workingday'] == "Libur"]['cnt'].max())]
significant_drop_hour_holiday = hourly_trend.loc[(hourly_trend['workingday'] == "Libur")].copy()
significant_drop_hour_holiday['drop'] = significant_drop_hour_holiday['cnt'].diff()
significant_drop_hour_holiday = significant_drop_hour_holiday.loc[significant_drop_hour_holiday['drop'].idxmin()]

total_rentals = hourly_trend['cnt'].sum()

# Menampilkan analisis
st.write("### Analisis:")
st.write(f"Pada rentang waktu dari **{start_date}** hingga **{end_date}**, terdapat **{total_rentals}** peminjaman sepeda yang mana:")
st.write(f"- Pada jam **{peak_hour_workday['hr'].values[0]}** adalah jam puncak peminjaman sepeda pada **hari kerja**, dan penurunannya terjadi pada jam **{significant_drop_hour_workday['hr']}**.")
st.write(f"- Pada jam **{peak_hour_holiday['hr'].values[0]}** adalah jam puncak peminjaman sepeda pada **hari libur**, dan penurunannya terjadi pada jam **{significant_drop_hour_holiday['hr']}**.")

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