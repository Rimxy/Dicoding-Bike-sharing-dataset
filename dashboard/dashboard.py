import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

main_data = pd.read_csv('dashboard/main_data.csv')
main_data['dteday'] = pd.to_datetime(main_data['dteday'])

start_date = st.sidebar.date_input('Pilih Tanggal Mulai', value=main_data['dteday'].min())
end_date = st.sidebar.date_input('Pilih Tanggal Akhir', value=main_data['dteday'].max())

filtered_data = main_data[(main_data['dteday'] >= pd.to_datetime(start_date)) & (main_data['dteday'] <= pd.to_datetime(end_date))]

page = st.sidebar.selectbox("Pilih Grafik", ("Hubungan Suhu dan Jumlah Penyewaan",
                                             "Distribusi Suhu", 
                                               "Pengaruh Cuaca terhadap Jumlah Penyewaan", 
                                               "Hubungan Kelembaban dan Jumlah Penyewaan", 
                                               "Hubungan Kecepatan Angin dan Jumlah Penyewaan", 
                                               "Distribusi Jumlah Penyewaan berdasarkan Status Kerja",
                                               "Pengaruh Cuaca terhadap Penyewaan Sepeda Berdasarkan Jam Operasional",
                                               "Jumlah Penyewaan Berdasarkan Kategori Musim dan Cuaca"))

if page == "Hubungan Suhu dan Jumlah Penyewaan":
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='temp_x', y='cnt_x', hue='weathersit_x', data=filtered_data, palette='coolwarm')
    plt.title('Hubungan Suhu dan Cuaca terhadap Jumlah Penyewaan Sepeda')
    plt.xlabel('Suhu (°C)')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    plt.legend(title='Kondisi Cuaca')
    plt.show()
    st.pyplot(plt)

elif page == "Pengaruh Cuaca terhadap Jumlah Penyewaan":
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='weathersit_x', y='cnt_x', data=filtered_data, palette='coolwarm')
    plt.title('Pengaruh Kondisi Cuaca terhadap Jumlah Penyewaan Sepeda', fontsize=14, fontweight='bold')
    plt.xlabel('Kondisi Cuaca', fontsize=12)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()
    st.pyplot(plt)

elif page == "Distribusi Suhu":
    plt.figure(figsize=(10, 6))
    sns.histplot(filtered_data['temp_x'], bins=20, kde=True)
    plt.title('Distribusi Suhu')
    plt.xlabel('Suhu (°C)')
    plt.ylabel('Frekuensi')
    st.pyplot(plt)

elif page == "Hubungan Kelembaban dan Jumlah Penyewaan":
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='hum_x', y='cnt_x', hue='weathersit_x', data=filtered_data, palette='coolwarm', alpha=0.6)
    plt.title('Hubungan Kelembaban dan Jumlah Penyewaan Sepeda')
    plt.xlabel('Kelembaban (%)')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    plt.legend(title='Kondisi Cuaca')
    plt.grid(True)
    plt.show()
    st.pyplot(plt)

elif page == "Hubungan Kecepatan Angin dan Jumlah Penyewaan":
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='windspeed_x', y='cnt_x', hue='weathersit_x', data=filtered_data, palette='coolwarm', alpha=0.6)
    plt.title('Hubungan Kecepatan Angin dan Jumlah Penyewaan Sepeda')
    plt.xlabel('Kecepatan Angin (m/s)')
    plt.ylabel('Jumlah Penyewaan Sepeda')
    plt.legend(title='Kondisi Cuaca')
    plt.grid(True)
    plt.show()
    st.pyplot(plt)

elif page == "Distribusi Jumlah Penyewaan berdasarkan Status Kerja":
    plt.figure(figsize=(10, 6))
    sns.histplot(data=filtered_data, x='cnt_x', hue='workingday_x', multiple="stack", bins=30, palette='pastel')
    plt.title('Distribusi Jumlah Penyewaan Sepeda berdasarkan Status Kerja')
    plt.xlabel('Jumlah Penyewaan Sepeda')
    plt.ylabel('Frekuensi')
    plt.legend(title='Status Kerja', labels=['Hari Kerja', 'Hari Libur'])
    plt.show()
    st.pyplot(plt)

elif page == "Pengaruh Cuaca terhadap Penyewaan Sepeda Berdasarkan Jam Operasional":
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    plt.figure(figsize=(12, 8))
    sns.lineplot(x='hr', y='cnt_x', hue='weathersit_x', data=filtered_data, palette=colors, hue_order=[1, 2, 3, 4], marker="o")
    plt.title('Pengaruh Cuaca terhadap Penyewaan Sepeda Berdasarkan Jam Operasional', fontsize=14, fontweight='bold')
    plt.xlabel('Jam Operasional', fontsize=12)
    plt.ylabel('Jumlah Penyewaan Sepeda', fontsize=12)
    plt.legend(title='Kondisi Cuaca', loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(np.arange(0, 24, 1))
    plt.show()
    st.pyplot(plt)

elif page == "Jumlah Penyewaan Berdasarkan Kategori Musim dan Cuaca":
    st.title("Jumlah Penyewaan Berdasarkan Kategori Musim dan Cuaca")
    
    def categorize_season_weather(row):
        if row['season_x'] == 1:  
            return 'Spring Clear' if row['weathersit_x'] == 1 else 'Spring Cloudy'
        elif row['season_x'] == 2:  
            return 'Summer Clear' if row['weathersit_x'] == 1 else 'Summer Cloudy'
        elif row['season_x'] == 3:  
            return 'Fall Clear' if row['weathersit_x'] == 1 else 'Fall Cloudy'
        elif row['season_x'] == 4:  
            return 'Winter Clear' if row['weathersit_x'] == 1 else 'Winter Cloudy'

    filtered_data['season_weather'] = filtered_data.apply(categorize_season_weather, axis=1)

    rental_counts = filtered_data.groupby('season_weather')['cnt_x'].sum().reset_index()

    colors = ['skyblue'] * len(rental_counts)
    max_rental = rental_counts['cnt_x'].max()

    plt.figure(figsize=(10, 6))
    for i in range(len(rental_counts)):
        if rental_counts['cnt_x'][i] == max_rental:
            plt.bar(rental_counts['season_weather'][i], rental_counts['cnt_x'][i], color='orange')  
        else:
            plt.bar(rental_counts['season_weather'][i], rental_counts['cnt_x'][i], color='skyblue')  

    plt.xlabel('Kategori Musim dan Cuaca')
    plt.ylabel('Jumlah Penyewaan')
    plt.title('Jumlah Penyewaan Berdasarkan Kategori Musim dan Cuaca')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    st.pyplot(plt)

if __name__ == '__main__':
    st.write("Ferry Saputra")
