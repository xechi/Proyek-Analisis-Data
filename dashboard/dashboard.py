import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
 
# Judul dashboard
st.title('Dashboard Peminjaman Sepeda')
 
# Membaca data
@st.cache_data
def load_data():
    day_df = pd.read_csv('dashboard/day_clean.csv')
    hour_df = pd.read_csv('dashboard/hour_clean.csv')
    return day_df, hour_df
 
day_df, hour_df = load_data()
 
# Menampilkan dataset
st.subheader("Dataset Peminjaman Sepeda per Hari")
st.write(day_df.head())
 
st.subheader("Dataset Peminjaman Sepeda per Jam")
st.write(hour_df.head())
 
# Membuat visualisasi
st.subheader('Distribusi Jumlah Peminjaman Sepeda')
 
# Grafik distribusi peminjaman sepeda
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(day_df['count'], bins=30, kde=True, ax=ax)
ax.set_title('Distribusi Jumlah Peminjaman Sepeda')
st.pyplot(fig)
 
# Visualisasi pola peminjaman berdasarkan cuaca dan musim
st.subheader('Pola Penggunaan Sepeda Berdasarkan Musim dan Kondisi Cuaca')
 
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='season', y='count', data=day_df, hue='weather_situation', ax=ax)
ax.set_title('Pola Penggunaan Sepeda Berdasarkan Musim dan Cuaca')
st.pyplot(fig)
 
# Visualisasi peminjaman berdasarkan jam
st.subheader('Pola Penggunaan Sepeda Berdasarkan Jam')
 
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='hour', y='count', data=hour_df, ax=ax)
ax.set_title('Jumlah Peminjaman Sepeda Berdasarkan Jam')
st.pyplot(fig)
 
# Visualisasi peminjaman berdasarkan hari dalam seminggu
st.subheader('Pola Penggunaan Sepeda Berdasarkan Hari dalam Seminggu')
 
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='day_of_week', y='count', data=day_df, ax=ax)
ax.set_title('Jumlah Peminjaman Sepeda Berdasarkan Hari dalam Seminggu')
st.pyplot(fig)