import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema Seaborn
sns.set_theme(style="dark")

# Fungsi untuk membuat DataFrame jumlah penyewaan sepeda harian
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Fungsi untuk membuat DataFrame jumlah penyewaan sepeda berdasarkan musim dan kondisi cuaca
def create_season_weather_rent_df(df):
    season_weather_df = df.groupby(['season', 'weather_situation'])['count'].mean().reset_index()
    return season_weather_df

# Fungsi untuk membuat DataFrame jumlah penyewaan sepeda berdasarkan jam
def create_hourly_rent_df(df):
    hourly_rent_df = df.groupby('hour')['count'].mean().reset_index()
    return hourly_rent_df

# Fungsi untuk membuat DataFrame jumlah penyewaan sepeda berdasarkan hari dalam seminggu
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby('day_of_week')['count'].mean().reset_index()
    return weekday_rent_df

# Membaca dataset dari file CSV
day_df = pd.read_csv('dashboard/day_clean.csv')
hour_df = pd.read_csv('dashboard/hour_clean.csv')

# Mengonversi kolom 'dateday' menjadi tipe datetime untuk mempermudah analisis berbasis waktu
day_df['dateday'] = pd.to_datetime(day_df['dateday'])
hour_df['dateday'] = pd.to_datetime(hour_df['dateday'])

# Mengurutkan data berdasarkan tanggal dan mereset index
day_df.sort_values(by="dateday", inplace=True)
day_df.reset_index(inplace=True)

# Sidebar untuk memilih rentang waktu filter
min_date_days = day_df["dateday"].min()  # Tanggal minimum dari data harian
max_date_days = day_df["dateday"].max()  # Tanggal maksimum dari data harian

min_date_hour = hour_df["dateday"].min()  # Tanggal minimum dari data per jam
max_date_hour = hour_df["dateday"].max()  # Tanggal maksimum dari data per jam

with st.sidebar:
    # Menambahkan logo perusahaan di sidebar
    st.image("https://st4.depositphotos.com/1588812/26966/v/450/depositphotos_269662818-stock-illustration-logo-for-bicycle-rental-vector.jpg")
    
    # Input rentang tanggal yang digunakan untuk filter data
    start_date, end_date = st.date_input(
        label='Rentang Waktu', 
        min_value=min_date_days, 
        max_value=max_date_days, 
        value=[min_date_days, max_date_days]
    )

# Menyaring data berdasarkan rentang tanggal yang dipilih
main_df_days = day_df[(day_df["dateday"] >= str(start_date)) & (day_df["dateday"] <= str(end_date))]
main_df_hour = hour_df[(hour_df["dateday"] >= str(start_date)) & (hour_df["dateday"] <= str(end_date))]

# Menyiapkan DataFrames berdasarkan data yang sudah difilter
daily_rent_df = create_daily_rent_df(main_df_days)
season_weather_df = create_season_weather_rent_df(main_df_days)
hourly_rent_df = create_hourly_rent_df(main_df_hour)
weekday_rent_df = create_weekday_rent_df(main_df_days)

# Header Dashboard
st.title('Dashboard Penyewaan Sepeda 🚴')

# Judul untuk analisis penyewaan sepeda bulanan
st.header("Analisis Penyewaan Sepeda Bulanan")

# Menampilkan total peminjaman sepeda secara keseluruhan
total_rent_count = daily_rent_df['count'].sum()
st.subheader('Peminjaman Harian')
col1, col2, col3 = st.columns(3)

with col1:
    st.metric('Total Penyewaan Sepeda', value=total_rent_count)  # Menampilkan total peminjaman sepeda

# Tabs untuk pertanyaan bisnis
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])

# Pertanyaan 1: Pola penggunaan sepeda berdasarkan musim dan cuaca
with tab1:
    st.header("Pertanyaan 1")
    st.subheader("Bagaimana pola penggunaan sepeda berdasarkan musim dan kondisi cuaca?")
    
    # Membuat plot: Pola penggunaan sepeda berdasarkan musim dan kondisi cuaca
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='season', y='count', data=season_weather_df, hue='weather_situation', ax=ax)
    ax.set_title('Pola Penggunaan Sepeda Berdasarkan Musim dan Kondisi Cuaca')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Jumlah Peminjaman Sepeda')
    plt.tight_layout()
    st.pyplot(fig)  # Menampilkan grafik di Streamlit

# Pertanyaan 2: Penggunaan sepeda berdasarkan jam dan hari
with tab2:
    st.header("Pertanyaan 2")
    st.subheader("Pada jam berapa dan hari apa penggunaan sepeda paling tinggi?")
    
    # Grafik penggunaan sepeda berdasarkan jam
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='hour', y='count', data=hourly_rent_df, ax=ax)
    ax.set_title('Jumlah Peminjaman Sepeda Berdasarkan Jam')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Jumlah Peminjaman')
    plt.tight_layout()
    st.pyplot(fig)  # Menampilkan grafik di Streamlit

    # Grafik penggunaan sepeda berdasarkan hari dalam seminggu
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='day_of_week', y='count', data=weekday_rent_df, ax=ax)
    ax.set_title('Jumlah Peminjaman Sepeda Berdasarkan Hari dalam Seminggu')
    ax.set_xlabel('Hari dalam Seminggu')
    ax.set_ylabel('Jumlah Peminjaman')
    plt.tight_layout()
    st.pyplot(fig)  # Menampilkan grafik di Streamlit